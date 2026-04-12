"""
Task service layer.
"""
import time
from typing import Optional, List
from taskmd_lite.models import Task
from taskmd_lite.repository import TaskRepository

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get_all_tasks(self) -> List[Task]:
        doc = self.repo.load()
        self._repair_ids(doc) # Keep ids consistent
        return doc.tasks

    def _repair_ids(self, doc):
        """Assign IDs to tasks that don't have them."""
        # Find highest current ID number
        max_id = 0
        for task in doc.tasks:
            if task.id and task.id.startswith('t_'):
                try:
                    num = int(task.id[2:])
                    max_id = max(max_id, num)
                except ValueError:
                    pass
        
        changed = False
        for task in doc.tasks:
            if not task.id:
                max_id += 1
                task.id = f"t_{max_id:02d}"
                changed = True
                
        if changed:
            self.repo.save(doc)

    def add_task(self, name: str, section: str = "Uncategorized", sub: str = "General", 
                 due: Optional[str] = None, pri: Optional[int] = None, rem: Optional[str] = None):
        doc = self.repo.load()
        self._repair_ids(doc)
        
        max_id = 0
        for task in doc.tasks:
            if task.id and task.id.startswith('t_'):
                try:
                    max_id = max(max_id, int(task.id[2:]))
                except ValueError:
                    pass
        
        new_id = f"t_{max_id + 1:02d}"
        
        t = Task(name=name, section=section, sub=sub, id=new_id, due=due, pri=pri, rem=rem)
        doc.tasks.append(t)
        self.repo.save(doc)

    def change_status(self, task_id: str, new_status: str):
        doc = self.repo.load()
        for task in doc.tasks:
            if task.id == task_id or task.id == f"t_{int(task_id):02d}" if task_id.isdigit() else False:
                task.status = new_status
                break
        self.repo.save(doc)

    def set_metadata(self, task_id: str, field: str, value: str):
        doc = self.repo.load()
        for task in doc.tasks:
            if task.id == task_id or task.id == f"t_{int(task_id):02d}" if task_id.isdigit() else False:
                if field == "due":
                    task.due = value
                elif field == "rem":
                    task.rem = value
                elif field == "pri":
                    try:
                        task.pri = int(value)
                    except ValueError:
                        pass
                elif field == "name":
                    task.name = value
                break
        self.repo.save(doc)

    def remove_task(self, task_id: str):
        doc = self.repo.load()
        original_length = len(doc.tasks)
        doc.tasks = [t for t in doc.tasks if not (t.id == task_id or (task_id.isdigit() and t.id == f"t_{int(task_id):02d}"))]
        if len(doc.tasks) < original_length:
            self.repo.save(doc)

    def remove_done(self):
        doc = self.repo.load()
        before = len(doc.tasks)
        doc.tasks = [t for t in doc.tasks if t.status != "[x]"]
        removed = before - len(doc.tasks)
        if removed == 0:
            print("\033[93m[INFO] No completed tasks to remove.\033[0m")
            return
        self.repo.save(doc)
        print(f"\033[92m[OK] Removed {removed} completed task(s).\033[0m")

    def check_daily_reset(self):
        doc = self.repo.load()
        self._repair_ids(doc)
        
        from datetime import datetime
        today_str = datetime.now().strftime("%Y-%m-%d")
        if doc.last_run != today_str:
            daily_tasks = [t for t in doc.tasks if t.section.lower() == 'daily']
            if daily_tasks:
                print(f"\n\033[93m[SYSTEM PING] New day detected ({today_str}).\033[0m")
                try:
                    ans = input("Do you want to reset all 'Daily' tasks to incomplete [ ]? (y/n): ")
                except (EOFError, KeyboardInterrupt):
                    ans = 'n'
                if ans.strip().lower() == 'y':
                    for t in daily_tasks:
                        t.status = "[ ]"
                    print("\033[92m[OK] Daily tasks reset.\033[0m")
            doc.last_run = today_str
            self.repo.save(doc)
