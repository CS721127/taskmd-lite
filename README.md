# TaskMD Lite

A pure, markdown-native, interactive terminal task manager engineered for speed and workflow integration. 

## Features
- **Markdown-Native Storage**: Uses a strictly structured `tasks.md` file as its database. Edits synchronize perfectly.
- **Interactive Console Dashboard (REPL)**: An immersive command-line loop mimicking interactive terminal dashboards, capable of color-coded live list renderings and context-aware error traps.
- **Automated Workflow Resets**: Tracks `last_run` explicitly resolving midnight task rollovers automatically.
- **Robust Schema Overrides**: Uses standardized regex parsing cleanly isolating priorities `***`, dates, comments `<!-- ->`, and legacy list properties.

## Installation

```bash
git clone git@github.com:CS721127/taskmd-lite.git
cd taskmd-lite
pip install -e .
```

## Usage

Simply run:
```bash
tm
```
This safely delegates you into the `root@taskManager:~#` shell rendering a live dashboard tree.

Available subcommands (accessible standalone as `tm [command]` or interactively inside the REPL):

```
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
```

## Structure
Please refer to the `./docs` directory to view native architectural references and schema breakdowns.
