import pytest
from taskmd_lite.models import Task, TaskDocument
from taskmd_lite.writer import write_markdown

def test_writer_basic():
    doc = TaskDocument()
    t1 = Task(name="Task 1", section="Sec1", sub="Sub1", id="t_01", due="2026-01-01", pri=3, rem="hello world")
    t2 = Task(name="Task 2", section="Sec1", sub="Sub1", status="[-]")
    doc.tasks.extend([t1, t2])
    
    out = write_markdown(doc)
    
    assert "<!-- taskmd-lite:version=1 -->" in out
    assert "# Sec1" in out
    assert "## Sub1" in out
    # Verify quotes are well formed and output formatting matches desired shape
    assert '- [ ] Task 1 <!-- id:t_01, due:2026-01-01, pri:3, rem:"hello world" -->' in out
    assert '- [-] Task 2' in out
