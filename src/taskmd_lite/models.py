"""
Core data models for TaskMD Lite.
"""
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Task:
    name: str
    section: str = "Uncategorized"
    sub: str = "General"
    status: str = "[ ]"
    id: Optional[str] = None
    due: Optional[str] = None
    pri: Optional[int] = None
    rem: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None

@dataclass
class TaskDocument:
    version: str = "1"
    timezone: str = "UTC"
    last_run: str = "1970-01-01"
    tasks: List[Task] = field(default_factory=list)
