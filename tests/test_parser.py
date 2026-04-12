import pytest
from taskmd_lite.parser import parse_markdown

def test_parse_basic():
    content = """<!-- taskmd-lite:version=1 -->
<!-- taskmd-lite:timezone=UTC -->

# School
## DP1092
- [ ] Assignment 1 <!-- id:t_01, due:2026-04-20, pri:5 -->
- [-] Lab work <!-- id:t_02, rem:"Need tutor feedback" -->
- [x] Done work
"""
    doc = parse_markdown(content)
    assert doc.version == "1"
    assert doc.timezone == "UTC"
    assert len(doc.tasks) == 3
    
    t1 = doc.tasks[0]
    assert t1.section == "School"
    assert t1.sub == "DP1092"
    assert t1.name == "Assignment 1"
    assert t1.status == "[ ]"
    assert t1.id == "t_01"
    assert t1.due == "2026-04-20"
    assert t1.pri == 5

    t2 = doc.tasks[1]
    assert t2.status == "[-]"
    assert t2.rem == "Need tutor feedback"

    t3 = doc.tasks[2]
    assert t3.status == "[x]"
    assert t3.name == "Done work"

def test_parse_legacy_shorthand():
    content = """# Legacy
## Format
- Just a task
*** - Urgent task
** - [-] Working task <!-- pri:5 -->
"""
    doc = parse_markdown(content)
    assert len(doc.tasks) == 3
    t1 = doc.tasks[0]
    assert t1.name == "Just a task"
    assert t1.status == "[ ]"
    assert t1.pri is None

    t2 = doc.tasks[1]
    assert t2.name == "Urgent task"
    assert t2.pri == 3

    t3 = doc.tasks[2]
    assert t3.name == "Working task"
    assert t3.status == "[-]"
    assert t3.pri == 5 # Overridden by metadata or keeps metadata? Let's check parser logic.
    # Actually wait! The parser sets `task.pri = len(pri_str)`, then OVERWRITES it if `pri:5` metadata is present!
    # Because `if pri_str:` is before `if meta_str:`. Let's assert it is 5.

def test_parse_without_metadata():
    content = """# Section
## Sub
- [ ] Just a task
"""
    doc = parse_markdown(content)
    assert len(doc.tasks) == 1
    t = doc.tasks[0]
    assert t.name == "Just a task"
    assert t.id is None
