# TaskMD Lite CLI

## Interaction model

Lite supports both:

- `tm` dashboard / interactive mode
- direct subcommands

## Core commands

### Task operations
- `tm add`
- `tm edit <id>`
- `tm done <id>`
- `tm todo <id>`
- `tm half <id>`
- `tm rm <id>`

### Metadata
- `tm due <id> <date>`
- `tm rem <id> <text>`
- `tm pri <id> <level>`

### Views
- `tm list`
- `tm list --sort tree`
- `tm list --sort priority`
- `tm list --sort due`
- `tm list --sort name`

### File / editor
- `tm open`
- `tm validate`
- `tm reload`

## Lite philosophy for commands

Keep the command surface small, memorable, and close to the original script's mental model.
