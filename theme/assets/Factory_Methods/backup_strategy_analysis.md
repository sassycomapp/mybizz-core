# MyBizz Backup Strategy

## Three-Layer Safety Architecture

### Layer 1: Anvil History (Automatic)
- **Provider:** Anvil.works platform
- **Retention:** 48 hours automatic
- **Access:** Anvil Editor → App Settings → History
- **Use Case:** Quick undo recent changes (< 48 hours)
- **Limitations:** Time-limited, Anvil-managed
- **Advantage:** Automatic, no action required

### Layer 2: GitHub Version Control
- **Provider:** GitHub repository
- **Retention:** Permanent (full git history)
- **Access:** Git commands, GitHub web interface
- **Use Case:** Long-term version control, collaboration
- **Limitations:** Requires commit discipline, push to remote
- **Advantage:** Industry standard, full history

### Layer 3: Local Timestamped Backups
- **Provider:** Backup Manager Droid
- **Retention:** Manual management
- **Location:** `C:\_Data\MyBizz\Backup_CompleteRepos`
- **Use Case:** Instant restoration to known good state
- **Limitations:** Disk space, manual cleanup
- **Advantage:** Fastest restore (seconds), complete state capture

---

## Backup Triggers

### CRITICAL (Must Backup)
- Before integration tests (Data Tables risk)
- Before Data Tables schema changes (high risk)
- Before Anvil Uplink operations with write access

### RECOMMENDED (Should Backup)
- After all tests passing (known good state)
- After feature complete (milestone)
- After successful bug fix (verified solution)
- Before major refactoring (safety net)

### OPTIONAL
- End of day (Windows scheduler does this)
- Before code review (clean state)

---

## Backup Naming Convention

**Format:** `YYYY-MM-DD_HH-MM_description`

**Examples:**
- `20260201-1430_contacts-feature-complete`
- `20260201-0915_before-integration-tests`
- `20260131-1645_auth-working`

---

## Restoration Procedures

### Restore from Local Backup (Fastest)
```powershell
robocopy "C:\_Data\MyBizz\Backup_CompleteRepos\[backup_name]" "C:\_Data\MyBizz\mybizz-core" /MIR /COPY:DAT /R:2 /W:5
```

---

## Backup Validation

Before creating backup:
- ✅ All tests passing (0 failures)
- ✅ Clean git state (no uncommitted changes, or committed intentionally)
- ✅ Valid backup trigger present

Before allowing next operation:
- ✅ Backup created successfully
- ✅ Backup documented in dev_log.md
- ✅ Restoration command recorded

---

## Disk Space Management

**Retention Policy:**
- Keep all milestone backups (feature complete) 
- Milestone backup naming format: `20260131-1645_milestone_bookings_complete`
- Keep all "before integration test" backups until tests verified
- Monthly cleanup of intermediate checkpoints (> 30 days old)
- Estimated space: ~2-5 MB per backup

**Cleanup Procedure:**
- Review dev_log.md for backup importance
- Delete intermediate backups only
- Never delete milestone backups

---

## Integration with Development Workflow

**Standard Feature Implementation:**
1. Plan feature
2. Backup (before starting)
3. Extract pure logic + write tests
4. Backup (before integration tests)
5. Run integration tests
6. Backup (after feature complete)

**Standard Bug Fix:**
1. Reproduce bug + write test
2. Backup (before fix)
3. Implement fix
4. Verify all tests pass
5. Backup (after fix verified)

---

**Last Updated:** 2026-02-02
