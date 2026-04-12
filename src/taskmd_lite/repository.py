"""
File repository for TaskMD Lite.
"""
from pathlib import Path
from taskmd_lite.models import TaskDocument
from taskmd_lite.parser import parse_markdown
from taskmd_lite.writer import write_markdown

class TaskRepository:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self) -> TaskDocument:
        if not self.file_path.exists():
            return TaskDocument()
        content = self.file_path.read_text(encoding="utf-8")
        return parse_markdown(content)

    def save(self, doc: TaskDocument):
        content = write_markdown(doc)
        tmp_path = self.file_path.with_suffix('.tmp')
        
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path.write_text(content, encoding="utf-8")
            tmp_path.replace(self.file_path)
        except OSError as e:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
            raise Exception(f"Failed to save tasks: {e}")
