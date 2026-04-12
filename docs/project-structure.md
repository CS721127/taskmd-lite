# TaskMD Lite Project Structure

## Recommended repository layout

```text
TaskMD-Lite/
├─ pyproject.toml
├─ README-lite.md
├─ docs/
│  ├─ overview-lite.md
│  ├─ schema-lite.md
│  ├─ cli-lite.md
│  ├─ minimal-architecture-lite.md
│  └─ lite-roadmap.md
├─ examples/
│  └─ tasks.md
├─ src/
│  └─ taskmd_lite/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ config.py
│     ├─ models.py
│     ├─ parser.py
│     ├─ writer.py
│     ├─ repository.py
│     ├─ service.py
│     └─ paths.py
└─ tests/
│  ├─ test_parser.py
│  ├─ test_writer.py
│  └─ test_roundtrip.py
```

## Why this structure is enough

Lite only needs a small number of modules:

- `cli.py` for subcommands and main loop
- `config.py` for path resolution and defaults
- `models.py` for task data
- `parser.py` / `writer.py` for Markdown round-trip
- `repository.py` for safe file access
- `service.py` for task operations

## What is intentionally omitted

- no `sidecar_service.py`
- no `export_service.py`
- no `ai_service.py`
- no `integrations/` package
- no `plugins/` package
