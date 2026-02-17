# **Continue.dev Cheatsheet - MyBizz/Anvil Solo Dev**

## **🎯 QUICK ACCESS**
```
Ctrl+L          → Open/Close Continue sidebar
Ctrl+I          → Edit mode (highlight code → describe change)  
Ctrl+Enter      → Accept edit diff
Esc             → Reject edit diff
Tab             → Accept autocomplete
```

## **📱 CONTEXT COMMANDS (@ Mentions)**
```
@codebase       → Search entire mybizz-core repo
@openFiles      → Current open tabs  
@file filename  → Specific file (e.g. @file ContactListForm.py)
@folder src/    → Folder contents
@workspace      → Open VSCode workspace
@docs anvil     → Anvil.works / Material3 / Python docs
@diff           → Current Git changes
```

## **🔪 YOUR 11 SLASH COMMANDS**
```
# Documentation
/read-all-docs    → Read ALL 25 Anvil+MyBizz docs  
/search-docs      → Search documentation
/find-doc         → Search documentation

# Codebase Navigation  
/search-code      → Search codebase
 /explore-structure → Interactive package tree browser

# Development Workflow
/implement-feature → Phase/stage/task from 03_dev_plan.md
/fix-bug          → Debug + fix with standards check
/review-code      → Full Anvil/MyBizz compliance review

# Forms & Server
/create-form      → M3 form with self.item pattern
/create-server-function → @anvil.server.callable template
/extract-pure-logic → Pure testable business logic
/write-tests      → Unit tests for pure logic
```

## **⚙️ MODEL SELECTION**
```
Chat: DeepSeek R1 (Primary) | GLM-5 | Kimi K2.5 | Trinity Large (Free)
Edit: Qwen3 Coder (Edit) | Devstral (Fast Edit)  
Autocomplete: Devstral (Autocomplete)
```

## **📋 WORKFLOW EXAMPLE**
```
1. Ctrl+L → Select "DeepSeek R1 (Primary)"
2. @codebase "show server_code structure" 
3. /search-docs "NavigationLink"
4. Highlight function → Ctrl+I → "add docstrings + type hints"
5. Ctrl+Enter → Review in GitLens
6. git add . && git commit -m "feat: XYZ" && git push
```

## **🚀 PRO TIPS**
```
- /read-all-docs first for new tasks (loads 350+ rules context)
- @codebase for existing code questions
- Ctrl+I for surgical edits (safer than full rewrites)
- Use "Devstral (Autocomplete)" for inline Tab completion
- GitLens shows who wrote each line (you vs AI)
```

**Your setup = production-grade.** Slash commands follow your exact Anvil/MyBizz standards.