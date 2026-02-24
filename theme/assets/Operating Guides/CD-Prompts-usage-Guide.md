Prompts Setup Guide - CORRECTED
Corrected guide:

text
# Continue.dev Prompts Setup Guide

## 1. Folder Location
- **Workspace**: `.continue/prompts/` 
- **Global**: `~/.continue/prompts/`

## 2. File Format
**YAML** (`.yaml`) OR **Markdown** (`.prompt.md`)

**YAML Example** `my-prompt.yaml`:
```yaml
name: my-prompt
description: My prompt description
***
Prompt content here with {{selection}}
3. Invocation
@my-prompt (autocomplete works)

4. Variables
Variable	Description
{{selection}}	Selected code
{{filename}}	Current file
{{codebase}}	Codebase context
5. Best Practices
name required in frontmatter

One task per prompt

.continue/prompts/ in git repo

text

**Summary**: No folder moving needed. Rules + MCPs work together. Prompts use `.yaml` format.