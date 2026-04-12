# TaskMD Lite — Minimal Architecture

## High-level shape

Lite is no longer a raw single file, but it is still intentionally compact.

```mermaid
flowchart TD
    User[User / Editor] --> CLI[CLI]
    CLI --> Service[Task Service]
    Service --> Repo[Repository]
    Repo --> Parser[Parser / Writer]
    Parser --> File[(tasks.md)]
```

## Read / write flow

```mermaid
sequenceDiagram
    participant U as User
    participant C as CLI
    participant S as Service
    participant R as Repository
    participant P as Parser/Writer
    participant F as tasks.md

    U->>C: tm done <id>
    C->>S: mark task done
    S->>R: load and save tasks
    R->>P: parse/write markdown
    P->>F: safe write
```

## Why this is the right amount of structure

It gives the project:

- maintainable boundaries
- testable parser/writer logic
- clean packaging
- editor compatibility

without jumping into sidecars, connectors, or ecosystem features.
