# TaskMD Lite Schema

## Goal

Lite uses Markdown as the primary task format without introducing advanced sidecar or connector concepts.

## Primary file

```text
tasks.md
```

## Header metadata

```md
<!-- taskmd-lite:version=1 -->
<!-- taskmd-lite:timezone=Australia/Sydney -->
```

## Structure

```md
# School
## DP1092
- [ ] Assignment 1 <!-- id:t_01, due:2026-04-20, pri:5 -->
- [-] Lab work <!-- id:t_02, rem:"Need tutor feedback" -->
```

## Status markers

- `[ ]` = todo
- `[-]` = in progress
- `[x]` = done

## Supported metadata in Lite

- `id`
- `due`
- `pri`
- `rem`
- `created`
- `updated`

## Direct edit rules

- tasks written manually without `id` receive an ID when saved
- moving tasks across sections preserves identity if `id` stays the same
- duplicate IDs should be repaired
- non-task Markdown should be preserved where possible

## Lite boundary

The Lite schema does not include:

- sidecar references
- weight / risk fields
- export-specific fields
- connector-specific data
- AI-specific metadata
