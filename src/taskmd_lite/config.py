"""
Configuration loader.
"""
from pathlib import Path
from taskmd_lite.paths import get_default_task_file

class Config:
    def __init__(self):
        self.task_file: Path = get_default_task_file()

def load_config() -> Config:
    return Config()
