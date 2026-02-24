# Slash Commands Deprecation Guide: Transition to Prompts in Continue.dev

## Overview
Slash commands (e.g., `/explain`) in Continue.dev have been **deprecated** in favor of the more powerful and flexible **Prompts** system. Prompts allow for reusable, templated instructions that can be invoked easily in the chat interface.

This guide extracts key information on migrating to Prompts.

## 1. Folder Location
- **Global prompts**: `~/.continue/prompts/`
- **Project-local prompts**: `.continue/prompts/` (in your repository root)
- Prompts in subdirectories are supported for organization (e.g., `.continue/prompts/coding/explain.yaml` → invoked as `@coding.explain`)

## 2. File Format
Prompts can be defined in two formats:
- **YAML** (`.yaml` extension): Structured and recommended for complex prompts.
- **Markdown** (`.prompt.md` or `.md` with YAML frontmatter): For prompts with formatted examples.

### YAML Example
```yaml
name: explain-code
description: Explain the selected code
prompt: |
  Explain the following code step by step:
  
  ```${filename}
  ${selection}
  ```
  
  Make it clear for a junior developer.
```

### Markdown Example
```markdown
---
name: refactor
description: Refactor the selected code
---
Please refactor this code to be more efficient and readable:

{{selection}}
```

## 3. Prompt Invocation Syntax
- In the Continue chat input: `@prompt-name`
- With arguments: `@prompt-name arg1 arg2`
- Arguments are passed as `{{0}}`, `{{1}}`, etc., or named.
- Auto-complete available as you type `@`.

Example: `@explain-code` on selected code.

## 4. Variables and Templating
Uses **Handlebars** templating engine (`{{variable}}`).

### Common Built-in Variables
| Variable | Description |
|----------|-------------|
| `{{selection}}` | Currently selected text/code |
| `{{filename}}` | Path to active file |
| `{{cursor}}` | Position of cursor |
| `{{agent}}` | Previous agent response |
| `{{messages}}` | Full chat history as array |
| `{{0}}, {{1}}...` | Positional args from invocation |
| `@var` | Custom slash command vars (legacy) |

### Custom Context
- Prompts can access model context, codebase, etc.
- Use conditionals: `{{#if selection}}...{{/if}}`

Full list: See [Continue docs - Templates](https://docs.continue.dev/reference/Templates).

## 5. Best Practices
- **Naming**: Use descriptive, kebab-case names (e.g., `fix-bugs`, `add-tests`).
- **Description**: Always include a clear `description` for autocomplete tooltips.
- **Organization**: Use subfolders for categories (e.g., `prompts/testing/`, `prompts/docs/`).
- **Conciseness**: Keep prompts focused; chain if needed.
- **Testing**: Test prompts in chat; iterate based on outputs.
- **Migration from Slash Commands**:
  1. Locate old `~/.continue/config.json` slash_commands.
  2. Convert to YAML prompts.
  3. Delete old slash_commands entry.
  4. Restart Continue or reload config (Cmd/Ctrl + Shift + P > \"Continue: Reload Config\").
- **Advanced**: Use `model`, `max_tokens`, `temperature` in frontmatter for customization.
- **Sharing**: Prompts are git-friendly; share via repo or Continue Hub (if available).

## Migration Checklist
- [ ] Backup `~/.continue/config.json`.
- [ ] Convert slash_commands to prompts YAML/MD.
- [ ] Move to `.continue/prompts/`.
- [ ] Test invocation with `@name`.
- [ ] Remove old slash_commands from config.json.
- [ ] Reload Continue.

For latest details, refer to [Continue.dev Prompts Docs](https://docs.continue.dev/customize/prompts).

**Created: $(date)**