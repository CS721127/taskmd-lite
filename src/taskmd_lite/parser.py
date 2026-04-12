"""
Markdown parser for TaskMD Lite.
"""
import re
from typing import List, Tuple
from taskmd_lite.models import Task, TaskDocument

def parse_markdown(content: str) -> TaskDocument:
    doc = TaskDocument()
    lines = content.splitlines()
    
    current_section = "Uncategorized"
    current_sub = "General"
    
    # regex for headers
    re_section = re.compile(r'^#\s+(.+)$')
    re_subsection = re.compile(r'^##\s+(.+)$')
    
    # regex for document metadata
    re_doc_meta = re.compile(r'^<!--\s*taskmd-lite:([a-zA-Z0-9_]+)=(.+?)\s*-->$')
    
    # regex for task
    re_task = re.compile(r'^(\*+)?\s*-\s*(?:\[([ xX\-])\]\s+)?(.*?)(?:\s+<!--\s+(.+?)\s+-->)?$')
    
    for line in lines:
        line_s = line.strip()
        
        m_doc = re_doc_meta.match(line_s)
        if m_doc:
            key, val = m_doc.groups()
            if key == "version":
                doc.version = val
            elif key == "timezone":
                doc.timezone = val
            elif key == "last_run":
                doc.last_run = val
            continue
            
        m_sec = re_section.match(line_s)
        if m_sec:
            current_section = m_sec.group(1).strip()
            current_sub = "General"
            continue
            
        m_sub = re_subsection.match(line_s)
        if m_sub:
            current_sub = m_sub.group(1).strip()
            continue
            
        m_task = re_task.match(line_s)
        if m_task:
            pri_str, status_char, name, meta_str = m_task.groups()
            
            status_char = status_char if status_char else " "
            status = f"[{status_char}]"
            
            task = Task(name=name.strip(), section=current_section, sub=current_sub, status=status)
            
            if pri_str:
                task.pri = len(pri_str)
            
            if meta_str:
                # Parse commas, but avoid splitting inside quotes
                # e.g. id:t_01, due:2026-04-20, pri:5, rem:"Text here"
                # A simple regex for key-value:
                # key:value OR key:"value"
                parts = re.findall(r'(\w+):"(.*?)"|(\w+):([^,}]+)', meta_str)
                for p in parts:
                    k1, v1, k2, v2 = p
                    k = k1 or k2
                    v = v1 if k1 else v2
                    k = k.strip()
                    v = v.strip()
                    if k == "id":
                        task.id = v
                    elif k == "due":
                        task.due = v
                    elif k == "pri":
                        try:
                            task.pri = int(v)
                        except ValueError:
                            pass
                    elif k == "rem":
                        task.rem = v
                    elif k == "created":
                        task.created = v
                    elif k == "updated":
                        task.updated = v

            doc.tasks.append(task)
            
    return doc
