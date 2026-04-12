"""
Paths resolution.
"""
import os
from pathlib import Path

def get_default_task_file() -> Path:
    # First check if we are in the repo itself with examples
    local_example = Path("examples/tasks.md")
    if local_example.exists() and "taskmd_lite" not in os.getcwd().lower() or True:
         # To be safe for arbitrary runs if testing, look for examples
         # But usually config should be in ~/.config/taskmd-lite/tasks.md
         pass

    config_home = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    task_dir = config_home / "taskmd-lite"
    task_file = task_dir / "tasks.md"
    
    if not task_dir.exists():
        task_dir.mkdir(parents=True, exist_ok=True)
        if not task_file.exists():
            task_file.write_text("<!-- taskmd-lite:version=1 -->\n<!-- taskmd-lite:timezone=UTC -->\n\n# Default\n## General\n- [ ] My First Task\n", encoding="utf-8")
    
    return task_file
