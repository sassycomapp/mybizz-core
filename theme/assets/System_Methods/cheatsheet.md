# **Continue.dev Cheatsheet - MyBizz/Anvil Solo Dev**

## **🎯 QUICK ACCESS**
```
Ctrl+L          → Open/Close Continue sidebar
Ctrl+I          → Edit mode (highlight code → describe change)  
Ctrl+Enter      → Accept edit diff
Esc             → Reject edit diff
Tab             → Accept autocomplete suggestion
Ctrl+Shift+P    → Command Palette (access all Continue commands)
```

---

## **🤖 YOUR MODELS - WHAT EACH ONE DOES**

### **Primary Development Model**
```
gpt-5.2-codex
├─ chat           → All planning, Q&A, architecture discussions
├─ edit           → Code modifications, refactoring
└─ summarize      → Condensing documentation, code review summaries

Use for: Everything except autocomplete, apply, embed, rerank
Confidence Score: +3.8 (highest in your stack)
```

### **Fallback / External Research**
```
claude-sonnet-4.6
├─ chat           → Deep thinking when gpt-5.2-codex struggles
└─ External only  → Use in claude.ai, NOT in Continue.dev workflow

Use for: Complex architecture decisions, research reports
Confidence Score: N/A (external tool)
```

### **Support Models (Background Workers)**
```
morph-v3-large
└─ apply          → Automatically applies code changes to files
                    (Invisible to you - Continue handles this)

codestral-2508
└─ autocomplete   → Tab completions while typing
                    (Low-latency, appears as you type)

text-embedding-3-small
└─ embed          → Powers @codebase search
                    (Invisible - handles semantic code search)

voyage-rerank-2
└─ rerank         → Improves @codebase search quality
                    (Optional - requires VoyageAI account)
```

### **Free Inspection Model**
```
Llama 4 Maverick
└─ chat           → Quick code inspection, casual questions
                    Free tier - use for low-stakes queries only
```

---

## **📱 CONTEXT COMMANDS (@ Mentions)**
```
@codebase       → Search entire mybizz-core repo (uses embedding model)
@file filename  → Specific file (e.g., @file ContactListForm.py)
@folder src/    → Folder contents
@openFiles      → All currently open tabs in VSCode  
@docs anvil     → Anvil.works / Material3 / Python documentation
@diff           → Current uncommitted Git changes
@workspace      → Open VSCode workspace files
```

**Pro Tip:** Start with `@codebase` for questions about existing code structure.

---

## **🔪 YOUR 11 SLASH COMMANDS**

### **Documentation Navigation**
```
/read-all-docs    → Read ALL 25+ Anvil + MyBizz CoP files
                    (Do this FIRST for any new feature)
                    
/search-docs      → Search documentation by keyword
                    (e.g., /search-docs NavigationLink)
                    
/find-doc         → Locate specific documentation file
```

### **Codebase Navigation**
```
/search-code      → Search all Python files for patterns
                    (e.g., @anvil.server.callable, app_tables)
                    
/explore-structure → Browse client_code/ and server_code/ packages
                     interactively
```

### **Development Workflow**
```
/implement-feature → Build feature from 03_dev_plan.md
                     (Reads CoP, creates files, follows M3 standards)
                     
/fix-bug          → Debug + fix with standards compliance check
                    (Asks for symptoms, locates root cause, applies fix)
                    
/review-code      → Full Anvil/MyBizz compliance audit
                    (Checks: Data Tables, M3 components, docstrings, etc.)
```

### **Code Generation**
```
/create-form            → Generate M3 form with self.item pattern
                          (Handles NavigationLink, data binding, etc.)
                          
/create-server-function → Server module template
                          (@anvil.server.callable + docstrings + logging)
                          
/extract-pure-logic     → Separate business logic for testing
                          (No Anvil imports, fully testable)
                          
/write-tests           → Unit tests for pure logic functions
                         (Server Console compatible)
```

---

## **⚙️ MODEL SWITCHING IN CONTINUE**

**When to switch:**
- **99% of the time:** Use `gpt-5.2-codex` (already selected by default)
- **Quick inspections:** Switch to `Llama 4 Maverick` to save costs
- **Deep research:** Don't switch — use claude.ai externally instead

**How to switch:**
1. Click model name dropdown in Continue sidebar (top)
2. Select new model
3. Start new conversation

**You do NOT manually select:**
- `morph-v3-large` (auto-triggered when applying changes)
- `codestral-2508` (auto-triggered on Tab keypress)
- `text-embedding-3-small` (auto-triggered by @codebase)
- `voyage-rerank-2` (auto-triggered by @codebase if configured)

---

## **🐙 GIT COMMANDS (Essential Daily Workflow)**

### **Check Status**
```powershell
git status                    # See what changed
git diff                      # See exact changes (line by line)
git log --oneline -5          # See last 5 commits
```

### **Save Your Work (Standard Flow)**
```powershell
git add .                     # Stage all changes
git commit -m "feat: add booking form"    # Commit with message
git push origin master        # Push to GitHub
```

### **Commit Message Prefixes (Use These)**
```
feat: XYZ        → New feature
fix: XYZ         → Bug fix
refactor: XYZ    → Code restructure (no behavior change)
docs: XYZ        → Documentation only
style: XYZ       → Formatting, whitespace
test: XYZ        → Adding tests
```

### **Undo Mistakes (Safe)**
```powershell
git reset                     # Unstage files (keeps changes)
git restore filename.py       # Discard changes in one file
git restore .                 # Discard ALL uncommitted changes (⚠️ permanent)
git rebase --abort            # Abort a merge conflict
```

### **Sync with GitHub**
```powershell
git pull origin master        # Download latest from GitHub
git fetch origin              # Check for changes (doesn't apply them)
```

### **Force Push (Use with Caution)**
```powershell
git push --force-with-lease origin master    # Overwrite GitHub with local
                                              # (Only if you're CERTAIN)
```

### **View Current Branch**
```powershell
git branch                    # Shows current branch with *
```

---

## **📋 TYPICAL WORKFLOW EXAMPLE**

### **Scenario: Implement Phase 3 Task (Add Payment Gateway)**

```
1. Ctrl+L → Select "gpt-5.2-codex"

2. Type: /read-all-docs
   (Loads all 350+ rules into context)

3. Type: @codebase show server_code/server_payments structure

4. Type: /implement-feature Phase 3.1 - Stripe Integration
   (Continue reads dev plan, creates files, follows CoP)

5. Review generated code in VSCode

6. Highlight any function → Ctrl+I → "add type hints and docstring"

7. Ctrl+Enter to accept changes

8. Test in Anvil (F5 to run)

9. Git workflow:
   git status
   git add .
   git commit -m "feat: add Stripe payment integration"
   git push origin master

10. Anvil auto-syncs from GitHub ✓
```

---

## **🚀 PRO TIPS**

### **Before Starting Any Task**
```
1. /read-all-docs               (Loads all standards)
2. @codebase [your question]    (Check existing code first)
3. Ask gpt-5.2-codex            (Plan before coding)
```

### **Editing Existing Code**
```
- Use Ctrl+I for surgical edits (safer than full rewrites)
- Always highlight the specific function/block you want changed
- Review diffs carefully before Ctrl+Enter
```

### **When gpt-5.2-codex Struggles**
```
- Rephrase your question more specifically
- Add more context with @ mentions
- Break complex tasks into smaller steps
- Use claude.ai externally for deep architecture analysis
```

### **Cost Management**
```
- Use "Llama 4 Maverick" for casual code inspections
- Reserve gpt-5.2-codex for actual development work
- claude-sonnet-4.6 stays external (use claude.ai interface)
```

### **Autocomplete Best Practices**
```
- Let codestral-2508 suggest (it's automatic on Tab)
- Review suggestions before accepting
- Autocomplete is inherently supervised (you review every line)
```

---

## **⚠️ CRITICAL REMINDERS**

### **NEVER Do These**
```
❌ Access app_tables from client code (server-only!)
❌ Use Anvil Extras components (M3 only!)
❌ Set click handlers on NavigationLink (use navigate_to property)
❌ Use print() in server code (use logging instead)
❌ Hardcode API keys (use secrets)
❌ Auto-commit without testing
```

### **ALWAYS Do These**
```
✅ Test before git push
✅ Read /read-all-docs for new features
✅ Use @codebase before asking questions
✅ Add docstrings + type hints to server functions
✅ Extract pure logic for testing
✅ Use self.item pattern for forms
✅ Check git status before committing
```

---

## **🔧 TROUBLESHOOTING**

### **Continue.dev Not Responding**
```
1. Check bottom-right of VSCode for Continue status
2. Ctrl+Shift+P → "Continue: Reload"
3. Restart VSCode completely
4. Check .continue/.env has correct API keys
```

### **Autocomplete Not Working**
```
1. Verify codestral-2508 is in config.yaml with autocomplete role
2. Check OpenRouter API key is valid
3. Restart VSCode
```

### **@codebase Returns No Results**
```
1. Verify text-embedding-3-small is configured
2. Wait for initial indexing (can take 30 seconds first time)
3. Try more specific search terms
```

### **Git Push Fails**
```
1. git pull origin master (sync first)
2. Resolve any conflicts
3. git push origin master (try again)
```

---

## **📞 QUICK REFERENCE LINKS**

**Documentation Locations:**
```
Anvil CoP:  C:\_Data\_Mybizz\mybizz-core\theme\assets\dev-docs\Anvil_Methods\
MyBizz Specs: C:\_Data\_Mybizz\mybizz-core\theme\assets\dev-docs\Mybizz_Methods\
```

**Key Files:**
```
config.yaml:     C:\Users\dev-p\.continue\config.yaml
.env secrets:    C:\Users\dev-p\.continue\.env
Dev Plan:        03_dev_plan.md (10 phases, 350+ tasks)
Architecture:    04_architecture_specification.md
CoP Coding:      anvil_cop_coding.md
```

**Models Dashboard:**
```
OpenRouter:      https://openrouter.ai/
VoyageAI:        https://www.voyageai.com/ (rerank - optional)
```

---

Inspect environment variables in PowerShell:

Quick Commands
text
# List ALL environment variables
Get-ChildItem Env:

# Search specific variable (e.g., OPENROUTER_API_KEY)
$Env:OPENROUTER_API_KEY

# Filter containing text
Get-ChildItem Env: | Where-Object Name -like "*OPENROUTER*"

# Export to file for review
Get-ChildItem Env: | Export-Csv -Path $HOME\Desktop\env-vars.csv -NoTypeInformation
Continue.dev Specific
text
# VSCode/Continue terminal check
code --list-extensions | Select-String continue
$Env:CONTINUE_CONFIG_FILE

# OpenRouter key verification
$Env:OPENROUTER_API_KEY ? "✅ Key loaded" : "❌ Missing"
Pro tip: Run notepad $PROFILE to edit PowerShell profile for permanent vars. Reload with . $PROFILE. Your config.yaml will pick them up automatically.

---
**Version:** 1.0  
**Last Updated:** February 18, 2026  
**Your setup:** Production-grade. Single-model workflow (gpt-5.2-codex). Test before push. No auto-commits.
