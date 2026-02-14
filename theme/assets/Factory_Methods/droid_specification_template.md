# DROID SPECIFICATION TEMPLATE
## Factory.AI Custom Droid Configuration

**Version:** 1.0  
**Date:** February 1, 2026  
**Purpose:** Modular template for defining custom droids for Mybizz development

---

## DROID: [DROID_NAME]

### 1. BASIC INFORMATION

**Droid Name:** [lowercase-hyphenated-name]  
**Display Name:** [Human Readable Name]  
**Category:** [Anvil Methods | Mybizz Methods | Factory Methods]  
**Description:** [50-100 word description of what this droid does]

**Primary Function:**  
[What is this droid's main job? 1-2 sentences]

**Scope:**  
[What is this droid allowed to do? What are its boundaries?]

---

### 2. FACTORY CONFIGURATION

#### File Location
- **Project Scope:** `.factory/droids/[droid-name].md`
- **Personal Scope:** `~/.factory/droids/[droid-name].md`
- **Recommended:** [Project | Personal]

#### Model Selection
```yaml
model: [inherit | claude-sonnet-4-5-20250929 | claude-opus-4-5-20251101 | custom:model-name]
```

**Rationale:** [Why this model choice?]

#### Reasoning Effort (if applicable)
```yaml
reasoningEffort: [low | medium | high]
```

**When to use:** [Explain when reasoning effort applies]

---

### 3. TOOLS CONFIGURATION

#### Tool Strategy
- [ ] **All tools** (omit tools field)
- [ ] **Category** (read-only | edit | execute | web | mcp)
- [ ] **Explicit list** (specific tool IDs)

#### Selected Tools
```yaml
tools: [
  "Read",
  "Write",
  "Edit",
  "Grep",
  "Glob",
  "Execute",
  "WebSearch",
  "FetchUrl"
]
```

**Rationale:** [Why these specific tools? What safety considerations?]

**Security Notes:**  
[Any tool restrictions for safety? What this droid should NEVER do?]

---

### 4. SKILLS CONFIGURATION

#### Required Skills
**Location:** `.factory/skills/[skill-name]/`

**Skills this droid uses:**
1. **[Skill Name 1]** - `skills/[skill-folder-1]/`
   - Purpose: [What this skill does]
   - When invoked: [Trigger conditions]

2. **[Skill Name 2]** - `skills/[skill-folder-2]/`
   - Purpose: [What this skill does]
   - When invoked: [Trigger conditions]

**Skills to create:** [List any new skills that need to be created for this droid]

---

### 5. DOCUMENT DEPENDENCIES

#### Primary Documents (from Document-to-Droid mapping)
**This droid's PRIMARY responsibility documents:**
1. [Document name] - [Why primary]
2. [Document name] - [Why primary]

#### Reference Documents
**This droid READS for context:**
1. [Document name] - [What context it provides]
2. [Document name] - [What context it provides]

#### Universal Documents (all droids read)
- [ ] 02_dev_policy.md
- [ ] Anvil_Based_Droid_Design_CoP.md
- [ ] anvil_cop_dev_log.md
- [ ] Factory_Context_Management_Guide.md
- [ ] Mastering_AI_Coding_-_Factory_Method.md

---

### 6. MCP INTEGRATIONS

#### Required MCPs
**This droid needs these MCP servers:**
- [ ] **[MCP Name]** - [Purpose for this droid]
- [ ] **[MCP Name]** - [Purpose for this droid]

**Configuration notes:** [Any special MCP setup needed]

---

### 7. HOOKS CONFIGURATION

#### Custom Hooks (if any)
**Hook events this droid uses:**

**PreToolUse:**
- Matcher: [tool pattern]
- Command: [hook command]
- Purpose: [Why this hook]

**PostToolUse:**
- Matcher: [tool pattern]
- Command: [hook command]
- Purpose: [Why this hook]

**Other hooks:** [Notification, Stop, SessionStart, etc.]

**No hooks required:** [ ] (check if droid doesn't need custom hooks)

---

### 8. SYSTEM PROMPT

#### Core Instructions
```markdown
You are [Droid Name], specialized in [primary function].

## Your Role
[2-3 sentences describing the droid's role in the development workflow]

## Your Responsibilities
1. [Primary responsibility 1]
2. [Primary responsibility 2]
3. [Primary responsibility 3]

## Your Constraints
1. [What you MUST do]
2. [What you MUST NOT do]
3. [Safety boundaries]

## Working Method
[How this droid approaches tasks - step-by-step if needed]

### When to delegate to other droids
- Delegate to [Other Droid Name] when: [condition]
- Delegate to [Other Droid Name] when: [condition]

## Success Criteria
You know you've succeeded when:
1. [Success criterion 1]
2. [Success criterion 2]
3. [Success criterion 3]

## References
You have access to these key documents:
- [Document 1]: [What to use it for]
- [Document 2]: [What to use it for]
```

---

### 9. INTERACTION PATTERNS

#### How to invoke this droid
**Manual invocation:**
```
"Use the [droid-name] droid to [task description]"
```

**Automatic triggers:**
- When [condition], main droid delegates to this droid
- When [condition], this droid is invoked

#### How this droid reports back
**Output format:**
```
Summary: [one-line finding]
Findings:
- [bullet point]
- [bullet point]

Recommendations:
- [action item]
- [action item]
```

#### Collaboration with other droids
- **Works with [Droid A]:** [How they collaborate]
- **Works with [Droid B]:** [How they collaborate]

---

### 10. GUARDRAILS & SAFETY

#### Critical Rules
1. **ALWAYS:** [Non-negotiable requirement 1]
2. **NEVER:** [Forbidden action 1]
3. **BEFORE [action]:** [Required precondition]

#### Escalation Triggers
**This droid stops and escalates when:**
- [Condition that requires human intervention]
- [Condition that requires another droid]
- [Unsafe condition detected]

#### Backup Integration
**Backup requirements:**
- [ ] Create backup before starting work
- [ ] Create backup after successful completion
- [ ] Update dev_log after each operation
- [ ] No backup required (read-only operations)

#### Testing Requirements
**Testing expectations:**
- [ ] Must run tests before completing
- [ ] Must create tests for new code
- [ ] Tests must pass before backup
- [ ] No testing required (non-code droid)

---

### 11. EXAMPLE USAGE

#### Use Case 1: [Scenario Name]
**Scenario:** [Description of when/why this droid is used]

**Input:** [What the droid receives]

**Process:** [Step-by-step what the droid does]

**Output:** [What the droid produces]

**Success indicators:** [How we know it worked]

---

#### Use Case 2: [Scenario Name]
**Scenario:** [Description of when/why this droid is used]

**Input:** [What the droid receives]

**Process:** [Step-by-step what the droid does]

**Output:** [What the droid produces]

**Success indicators:** [How we know it worked]

---

### 12. FACTORY FILE STRUCTURE

#### Complete Droid Definition (.md file)
```yaml
---
name: [droid-name]
description: [Brief description for UI display]
model: [inherit | specific-model]
reasoningEffort: [low | medium | high]  # Optional
tools: [tool-list or category]
---

# [Droid Name]

[Full system prompt from section 8 above]
```

#### Skills Folder Structure
```
.factory/skills/[droid-name]-skills/
├── SKILL.md or skill.mdx
├── references.md (optional)
├── schemas/ (optional)
└── checklists.md (optional)
```

---

### 13. VALIDATION CHECKLIST

**Before deploying this droid:**
- [ ] Name follows Factory naming conventions (lowercase, hyphens)
- [ ] Description under 500 characters
- [ ] Model specified or inherits appropriately
- [ ] Tools explicitly defined for safety
- [ ] All referenced skills exist
- [ ] All referenced documents exist
- [ ] System prompt is clear and complete
- [ ] Guardrails are explicit
- [ ] Example use cases provided
- [ ] No security vulnerabilities in tool access
- [ ] Backup integration defined
- [ ] Testing requirements clear
- [ ] Escalation paths defined

---

### 14. MAINTENANCE NOTES

#### Version History
| Version | Date | Changes | By |
|---------|------|---------|-----|
| 1.0 | [Date] | Initial creation | [Name] |

#### Known Issues
- [Issue 1]
- [Issue 2]

#### Future Enhancements
- [ ] [Enhancement 1]
- [ ] [Enhancement 2]

#### Review Schedule
- **Next review:** [Date]
- **Review frequency:** [Monthly | Quarterly | Per phase]

---

## COMPLETION STATUS

- [ ] Template populated
- [ ] Skills created
- [ ] Tools verified
- [ ] Documents accessible
- [ ] MCPs configured
- [ ] Hooks tested (if applicable)
- [ ] System prompt finalized
- [ ] Example usage validated
- [ ] Factory file created
- [ ] Droid tested in development
- [ ] Documentation complete
- [ ] Ready for production use

---

**END OF DROID SPECIFICATION TEMPLATE**

---

## TEMPLATE USAGE INSTRUCTIONS

**To create a new droid spec:**

1. Copy this template
2. Replace all `[BRACKETED_ITEMS]` with actual values
3. Check all checkboxes `[ ]` that apply
4. Fill in all sections completely
5. Validate against checklist (section 13)
6. Create the actual `.factory/droids/[name].md` file
7. Create required skills in `.factory/skills/`
8. Test the droid with simple tasks
9. Document results and iterate

**Critical sections that MUST be completed:**
- Section 1: Basic Information
- Section 2: Factory Configuration
- Section 3: Tools Configuration
- Section 5: Document Dependencies
- Section 8: System Prompt
- Section 10: Guardrails & Safety

**Optional but recommended:**
- Section 4: Skills (if droid uses skills)
- Section 6: MCP Integrations (if droid needs MCPs)
- Section 7: Hooks (if droid needs custom hooks)
- Section 11: Example Usage (helps validate droid design)
