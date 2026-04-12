# TaskMD Lite Roadmap

## Lite roadmap goal

Build the first clean GitHub version of the task manager without crossing into late-stage feature territory.

## Stage 1 — Projectization
- create package structure
- add `pyproject.toml`
- expose `tm` command
- move default file into config directory

## Stage 2 — Markdown-native storage
- define Lite schema
- build parser / writer
- replace TXT-style storage with `tasks.md`

## Stage 3 — Direct-edit compatibility
- auto ID enrichment
- duplicate ID repair
- safe writeback
- validation command

## Stage 4 — Core CLI usability
- add / edit / done / due / rem / remove
- list views and sorting
- `tm open`

## Stage 5 — Stabilization
- round-trip tests
- parser/writer tests
- README and docs polish
- freeze Lite scope

## What does not belong in Lite

- export layer
- sidecar system
- risk engine
- academic mode
- connectors
- remote backends
- AI
