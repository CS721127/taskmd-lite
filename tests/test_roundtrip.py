import pytest
from taskmd_lite.models import Task, TaskDocument
from taskmd_lite.writer import write_markdown
from taskmd_lite.parser import parse_markdown

def test_roundtrip():
    doc = TaskDocument()
    doc.version = "2"
    doc.timezone = "Europe/London"
    
    t1 = Task(name="Roundtrip Test 1", section="A", sub="B", status="[ ]", id="t_01", due="2026-10-10", pri=1, rem="remark text")
    t2 = Task(name="Roundtrip Test 2", section="A", sub="C", status="[x]", id="t_02")
    
    doc.tasks.extend([t1, t2])
    
    markdown_str = write_markdown(doc)
    
    parsed_doc = parse_markdown(markdown_str)
    
    assert parsed_doc.version == "2"
    assert parsed_doc.timezone == "Europe/London"
    assert len(parsed_doc.tasks) == 2
    
    pt1 = parsed_doc.tasks[0]
    assert pt1.name == t1.name
    assert pt1.section == t1.section
    assert pt1.sub == t1.sub
    assert pt1.status == t1.status
    assert pt1.id == t1.id
    assert pt1.due == t1.due
    assert pt1.pri == t1.pri
    assert pt1.rem == t1.rem

    pt2 = parsed_doc.tasks[1]
    assert pt2.name == t2.name
    assert pt2.section == t2.section
    assert pt2.sub == t2.sub
    assert pt2.status == t2.status
    assert pt2.id == t2.id
