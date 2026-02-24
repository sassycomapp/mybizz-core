# MyBizz Backup Strategy

**Last Updated:** 2026-02-21

---

## Overview

Five backup layers protect the project. Agents are only responsible for Layer 5.
All other layers are managed by you or automated systems.

---

## Layer 1: Anvil Platform (Automatic)
- **Who:** Anvil.works
- **What:** 48-hour rolling backup of the entire Anvil app
- **Action Required:** None
- **Restore:** Anvil Editor → App Settings → History

---

## Layer 2: Daily Scheduled Backup (Automatic)
- **Who:** Windows Task Scheduler
- **What:** Full local repo snapshot, daily at 17:00
- **Location:** `C:\_Data\_Mybizz\backup\`
- **Naming:** `mybizz-core_YYYY-MM-DD`
- **Action Required:** None (runs automatically)

---

## Layer 3: Pre-Work Backup (Manual — You)
Before starting any development session, you make a full backup of the local repo.

- **Location:** `C:\_Data\_Mybizz\backup\`
- **Naming:** `mybizz-core_(YYYYMMDD-HHMM)-PreWork`
- **Example:** `mybizz-core_(20260221-0900)-PreWork`

---

## Layer 4: Milestone Backups (Manual — You)
You make these at two specific moments in the agent workflow:

| Moment | Naming Convention | Example |
|--------|------------------|---------|
| After GLM Drafter completes | `mybizz-core_(YYYYMMDD-HHMM)-Draft-{feature}` | `mybizz-core_(20260221-1430)-Draft-auth` |
| After Claude Polisher completes | `mybizz-core_(YYYYMMDD-HHMM)-Done-{feature}` | `mybizz-core_(20260221-1600)-Done-auth` |

- **Location:** `C:\_Data\_Mybizz\backup\`

---

## Layer 5: Working File Backup (Agent Responsibility)
**This is the only layer the agents manage.**

Before editing any file, the agent saves a copy of the original to:

`C:\_Data\_Mybizz\mybizz-core\theme\assets\Backup_Temp\`

- **Naming:** `YYYYMMDD-HHMM_filename`
- **Example:** `20260221-1430_customer_service.py`
- **Purpose:** Instant rollback if the edit causes a problem
- **Cleanup:** Agent deletes these files after successful tests

---

## Standard Development Workflow

```
1. You make Pre-Work backup (Layer 3)
2. Agent backs up files before editing (Layer 5) — automatic
3. GLM Drafter completes work
4. You make Draft backup (Layer 4)
5. Claude Polisher reviews, fixes, tests
6. You make Done backup (Layer 4)
7. Agent cleans up Backup_Temp (Layer 5) — automatic
8. Daily backup runs at 17:00 (Layer 2) — automatic
```

---

## Emergency Recovery

| Problem | Solution |
|---------|----------|
| Bad edit during current session | Restore from `Backup_Temp` (Layer 5) |
| Need to undo last few hours | Restore from today's milestone backup (Layer 4) |
| Need yesterday's version | Restore from daily backup (Layer 3) |
| Anvil app corrupted | Restore from Anvil History (Layer 1) |
