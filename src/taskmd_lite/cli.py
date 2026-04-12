"""
Command Line Interface for TaskMD Lite.
"""
import argparse
import sys
import subprocess
import os
import shlex
import re
from datetime import datetime
from taskmd_lite.config import load_config
from taskmd_lite.repository import TaskRepository
from taskmd_lite.service import TaskService
from taskmd_lite.parser import parse_markdown

def get_time_left(due: str) -> str:
    if not due: return ""
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d")
        delta = due_date.date() - datetime.now().date()
        if delta.days < 0: return "\033[91m(OVERDUE)\033[0m"
        elif delta.days == 0: return "\033[91m(DUE TODAY)\033[0m"
        return f"\033[93m(⏳ {delta.days}d left)\033[0m"
    except ValueError:
        return "\033[91m(Invalid Date)\033[0m"

class TaskMDParser(argparse.ArgumentParser):
    def __init__(self, interactive=False, *args, **kwargs):
        self.interactive = interactive
        super().__init__(*args, **kwargs)

    def print_usage(self, file=None):
        usage_text = """usage: tm <command> [args]

  tm add [name] [-s section] [-b sub]      Launch task creation wizard or add task inline
  tm done <id>                             Mark task as completed [x]
  tm half <id>                             Mark task as in-progress [-]
  tm todo <id>                             Mark task as undone [ ]
  tm rm <id>                               Delete specific task
  tm rm_done                               Delete ALL completed tasks [x]
  tm edit <id> <name>                      Edit task name
  tm due <id> <YYYY-MM-DD>                 Set deadline
  tm rem <id> <text>                       Add/Edit remark for a task
  tm pri <id> <level>                      Edit task priority manually by integer level
  tm list [--sort tree|priority|due|name]  View tasks with specific sorting
  tm sort [-i|-p|-d|-n]                    Alias for list sorting (-i=tree, -p=priority, -d=due, -n=name)
  tm open                                  Open tasks markdown file in default editor (fallback to nano)
  tm validate                              Check markdown file for structural errors
  tm reload                                Reload tasks and repair tracking IDs automatically
  tm help                                  Show this help manual
  tm exit                                  Save and close REPL loop
"""
        if file is None:
            file = sys.stdout
        file.write(usage_text)

    def print_help(self, file=None):
        self.print_usage(file)

    def error(self, message):
        self.print_usage(sys.stdout)
        print(f"\033[91m[!] {message}\033[0m")
        if self.interactive:
            raise ValueError(message)
        else:
            sys.exit(1)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stdout)
        if self.interactive:
            raise RuntimeError("InteractiveContinue")
        else:
            sys.exit(status)

def get_parser(interactive=False):
    parser = TaskMDParser(interactive=interactive, description="TaskMD Lite CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("name", nargs="?", help="Task name")
    parser_add.add_argument("--section", "-s", default="Uncategorized")
    parser_add.add_argument("--sub", "-b", default="General")

    # Status changes
    for cmd in ["done", "half", "todo", "rm"]:
        p = subparsers.add_parser(cmd)
        p.add_argument("id", help="Task ID")

    # rm_done
    subparsers.add_parser("rm_done")

    # edit
    parser_edit = subparsers.add_parser("edit")
    parser_edit.add_argument("id")
    parser_edit.add_argument("name")

    # metadata
    p_due = subparsers.add_parser("due")
    p_due.add_argument("id")
    p_due.add_argument("date")

    p_rem = subparsers.add_parser("rem")
    p_rem.add_argument("id")
    p_rem.add_argument("text")

    p_pri = subparsers.add_parser("pri")
    p_pri.add_argument("id")
    p_pri.add_argument("level", type=int)

    # list
    p_list = subparsers.add_parser("list")
    p_list.add_argument("--sort", choices=["tree", "priority", "due", "name"], default="tree")

    # sort (alias for list --sort)
    p_sort = subparsers.add_parser("sort")
    p_sort.add_argument("mode", choices=["-i", "-p", "-d", "-n"], help="Sort mode")

    # file interactions
    subparsers.add_parser("open")
    subparsers.add_parser("validate")
    subparsers.add_parser("reload")
    
    # REPL specific
    subparsers.add_parser("help")
    subparsers.add_parser("exit")

    return parser

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def add_task_wizard(service):
    print("\n\033[96m[ADD TASK WIZARD]\033[0m")
    try:
        sec  = input("  Section (e.g. School)    : ").strip() or "Misc"
        sub  = input("  Subsection (e.g. DP1093) : ").strip() or "General"
        pri  = input("  Priority (e.g. ***)      : ").strip()
        name = input("  Task Name                : ").strip()

        if not name:
            print("\033[91m[!] Task name cannot be empty. Aborted.\033[0m")
            return

        if pri and not re.fullmatch(r'\*+', pri):
            print("\033[91m[!] Priority must contain only '*' characters (e.g. ***). Aborted.\033[0m")
            return

        while True:
            due = input("  Due Date (YYYY-MM-DD) [Optional]: ").strip()
            if not due:
                due = None
                break
            if is_valid_date(due):
                break
            print("\033[91m  [!] Invalid date format. Please try again or leave blank.\033[0m")

        rem = input("  Remark [Optional]: ").strip() or None

    except (EOFError, KeyboardInterrupt):
        print("\n\033[93m[INFO] Add task cancelled.\033[0m")
        return
        
    service.add_task(name, section=sec, sub=sub, due=due, pri=len(pri) if pri else None, rem=rem)
    print(f"\033[92m[OK] Task added.\033[0m")


def handle_args(args, service, config, parser):
    if args.command == "add":
        if not args.name:
            add_task_wizard(service)
        else:
            service.add_task(args.name, section=args.section, sub=args.sub)
            print("Task added.")
    
    elif args.command == "done":
        service.change_status(args.id, "[x]")
        print("Status updated.")
    elif args.command == "half":
        service.change_status(args.id, "[-]")
        print("Status updated.")
    elif args.command == "todo":
        service.change_status(args.id, "[ ]")
        print("Status updated.")
    elif args.command == "rm":
        service.remove_task(args.id)
        print("Task removed.")
    elif args.command == "rm_done":
        service.remove_done()
    elif args.command == "edit":
        service.set_metadata(args.id, "name", args.name)
        print("Name updated.")

    elif args.command == "due":
        if not is_valid_date(args.date):
            print("\033[91m[!] Invalid date format. Must be YYYY-MM-DD.\033[0m")
        else:
            service.set_metadata(args.id, "due", args.date)
            print("Due date updated.")
    elif args.command == "rem":
        service.set_metadata(args.id, "rem", args.text)
        print("Remark updated.")
    elif args.command == "pri":
        service.set_metadata(args.id, "pri", args.level)
        print("Priority updated.")
    
    elif args.command in ("list", "sort"):
        # Map sort argument back to list variables
        sort_mode = "tree"
        if args.command == "sort":
            msg_map = {"-i": "tree", "-p": "priority", "-d": "due", "-n": "name"}
            sort_mode = msg_map.get(args.mode, "tree")
        elif args.command == "list":
            sort_mode = args.sort

        tasks = service.get_all_tasks()
        
        mode_str = {
            "tree": "TREE_VIEW (CATEGORICAL)",
            "priority": "SORT BY PRIORITY",
            "due": "SORT BY DUE DATE",
            "name": "SORT BY NAME"
        }.get(sort_mode, "UNKNOWN_MODE")
        
        subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
        print("\033[96m" + "="*80 + "\033[0m")
        print(f" 📂 SOURCE: {config.task_file} | \033[1mMODE: {mode_str}\033[0m")
        print("\033[96m" + "="*80 + "\033[0m\n")
        
        def format_task(t):
            color = "\033[92m" if t.status == "[x]" else "\033[93m" if t.status == "[-]" else "\033[0m"
            pri_str = f"\033[91m{'*' * t.pri:<5}\033[0m" if t.pri else " "*5
            rem_info = f"  \033[90m<{t.rem}>\033[0m" if t.rem else ""
            time_left = get_time_left(t.due) if t.due else ""
            time_left_str = f" {time_left}" if time_left else ""
            return f"      \033[94m[{t.id}]\033[0m {pri_str} {color}{t.status}\033[0m {t.name}{time_left_str}{rem_info}"

        if sort_mode == "priority":
            tasks.sort(key=lambda t: t.pri or 0, reverse=True)
            for t in tasks:
                print(format_task(t))
        elif sort_mode == "due":
            tasks.sort(key=lambda t: t.due or "9999-99-99")
            for t in tasks:
                print(format_task(t))
        elif sort_mode == "name":
            tasks.sort(key=lambda t: t.name.lower())
            for t in tasks:
                print(format_task(t))
        else: # tree format
            hierarchy = {}
            for t in tasks:
                hierarchy.setdefault(t.section, {}).setdefault(t.sub, []).append(t)
            for sec, subs in hierarchy.items():
                print(f"\033[1m--- {sec}\033[0m")
                for sub, tlist in subs.items():
                    print(f"    \033[36m-- {sub}\033[0m")
                    for t in tlist:
                        print(format_task(t))
                        
        print("\n" + "-"*80)
        print(" \033[90mType 'help' for commands list | 'exit' to quit\033[0m")

    elif args.command == "open":
        print(f"Opening {config.task_file}...")
        editor = os.environ.get('EDITOR', 'nano')
        subprocess.run([editor, str(config.task_file)])

    elif args.command == "validate":
        try:
            service.repo.load()
            print("Validate OK.")
        except Exception as e:
            print(f"Validation failed: {e}")

    elif args.command == "reload":
        service.get_all_tasks()
        print("Reload complete and IDs repaired.")

    elif args.command == "help":
        parser.print_help()
        
    elif args.command == "exit":
        sys.exit(0)

def run_repl(service, config):
    parser = get_parser(interactive=True)
    
    # Run daily check automatically upon entering REPL
    service.check_daily_reset()
    
    # Initial print of the dashboard via list
    try:
        args_list = parser.parse_args(["list"])
        handle_args(args_list, service, config, parser)
    except Exception:
        pass
    
    while True:
        try:
            cmd_input = input("\nroot@taskManager:~# ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\033[93m[INFO] Exit via keyboard interrupt.\033[0m")
            break

        if not cmd_input:
            continue

        try:
            args = parser.parse_args(shlex.split(cmd_input))
            handle_args(args, service, config, parser)
        except ValueError:
            # Caught parser exception. Don't add 'Enter to continue', just roll over.
            pass
        except SystemExit as e:
            if e.code == 0:
                break
        except RuntimeError as e:
            if str(e) == "InteractiveContinue":
                pass
            else:
                raise
        except Exception as e:
            print(f"\033[91m[!] Error executing command: {e}\033[0m")


def main():
    config = load_config()
    repo = TaskRepository(config.task_file)
    service = TaskService(repo)

    if len(sys.argv) == 1:
        # Run REPL Mode
        run_repl(service, config)
    else:
        # Standard CLI mode
        parser = get_parser(interactive=False)
        try:
            args = parser.parse_args()
            if args.command:
                handle_args(args, service, config, parser)
        except SystemExit:
            pass

if __name__ == "__main__":
    main()
