"""
Markdown writer for TaskMD Lite.
"""
from taskmd_lite.models import TaskDocument

def write_markdown(doc: TaskDocument) -> str:
    lines = []
    lines.append(f"<!-- taskmd-lite:version={doc.version} -->")
    lines.append(f"<!-- taskmd-lite:timezone={doc.timezone} -->")
    lines.append(f"<!-- taskmd-lite:last_run={doc.last_run} -->")
    lines.append("")
    
    # Group tasks by section -> subsection
    hierarchy = {}
    for task in doc.tasks:
        sec = task.section or "Uncategorized"
        sub = task.sub or "General"
        if sec not in hierarchy:
            hierarchy[sec] = {}
        if sub not in hierarchy[sec]:
            hierarchy[sec][sub] = []
        hierarchy[sec][sub].append(task)
        
    for sec, subs in hierarchy.items():
        lines.append(f"# {sec}")
        for sub, tasks in subs.items():
            if sub != "General" or len(subs) > 1 or True: # Actually always write ##
                lines.append(f"## {sub}")
            for task in tasks:
                meta = []
                if task.id: meta.append(f"id:{task.id}")
                if task.due: meta.append(f"due:{task.due}")
                if task.pri is not None: meta.append(f"pri:{task.pri}")
                if task.rem:
                    clean_rem = task.rem.replace('"', '')
                    meta.append(f'rem:"{clean_rem}"')
                if task.created: meta.append(f"created:{task.created}")
                if task.updated: meta.append(f"updated:{task.updated}")
                
                meta_str = ""
                if meta:
                    meta_str = f" <!-- {', '.join(meta)} -->"
                
                status = task.status if task.status in ("[ ]", "[-]", "[x]") else "[ ]"
                lines.append(f"- {status} {task.name}{meta_str}")
        lines.append("")
        
    # Trim ending whitespace and add one newline
    while lines and not lines[-1].strip():
        lines.pop()
    
    return "\n".join(lines) + "\n"
