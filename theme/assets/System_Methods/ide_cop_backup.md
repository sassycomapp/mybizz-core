# MyBizz Backup Strategy

## Three-Layer Safety Architecture

### Layer 1: Anvil History (Automatic)
- **Provider:** Anvil.works platform
- **Retention:** 48 hours automatic
- **Access:** Anvil Editor → App Settings → History
- **Use Case:** Quick undo recent changes (< 48 hours)
- **Limitations:** Time-limited, Anvil-managed
- **Advantage:** Automatic, no action required
- **Trigger:** Automatic, Anvil-managed
- **Content:** Anvil Repo (including Data Tables schema)
- **Naming convention:** Anvil Managed

#### Verification Procedure
- Access Anvil Editor → App Settings → History
- Verify last backup timestamp is within expected timeframe
- Confirm you can see commit history for last 48 hours

#### Restore Method
1. Open Anvil Editor
2. Navigate to App Settings → History
3. Browse commit history
4. Click on desired commit to view changes
5. Use Anvil's restore functionality to revert to that state

#### Cleanup Procedure
- **Managed by:** Anvil.works platform
- **Action Required:** None - automatic 48-hour retention

---

### Layer 2: GitHub Version Control
- **Provider:** GitHub repository
- **Retention:** Permanent (full git history)
- **Access:** Git commands, GitHub web interface
- **Use Case:** Long-term version control, collaboration, disaster recovery
- **Limitations:** Requires commit discipline, push to remote
- **Advantage:** Industry standard, full history, offsite storage
- **Trigger:** Manual (git push after successful tests)
- **Content:** GitHub Repo (code, schema, configuration)
- **Naming Convention:** Git commit messages

#### Verification Procedure
```bash
# Verify local repo is in sync with GitHub
git status

# View recent commits
git log --oneline -10

# Verify last push timestamp
git log origin/main -1

# Check if local changes need to be pushed
git log origin/main..HEAD
```

#### Restore Method

**Restore Individual File:**
```bash
# View file history
git log --oneline -- path/to/file.py

# Restore specific file from specific commit
git checkout <commit-hash> -- path/to/file.py

# Restore file from previous commit
git checkout HEAD~1 -- path/to/file.py
```

**Restore Entire Repo to Previous State:**
```bash
# View commit history
git log --oneline

# Create new branch from specific commit (safe method)
git checkout -b recovery-branch <commit-hash>

# Or reset current branch to specific commit (destructive)
git reset --hard <commit-hash>

# If you've already pushed bad code, revert it
git revert <bad-commit-hash>
git push origin main
```

**Undo Last Local Commit (not pushed):**
```bash
# Keep changes in working directory
git reset --soft HEAD~1

# Discard changes completely
git reset --hard HEAD~1
```

#### Cleanup Procedure
- **Managed by:** GitHub
- **Action Required:** None - Git maintains full history
- **Optional:** Periodically review and squash old feature branches

---

### Layer 3: Auto Scheduled Backups
- **Provider:** Windows Scheduled Task
- **Retention:** Manual management (keep 7-30 days recommended)
- **Location:** `C:\_Data\_Mybizz\backup\`
- **Schedule:** Daily at 17:00 (5:00 PM)
- **Scope:** mybizz-core repository only
- **Use Case:** Daily safety net, quick recovery to yesterday's state
- **Limitations:** Disk space, manual cleanup required
- **Advantage:** Fast restore, automatic daily capture
- **Trigger:** Time-based (Windows Task Scheduler)
- **Content:** Complete local repo snapshot
- **Naming Convention:** `mybizz-core_YYYY-MM-DD` (Windows file timestamp provides time)
  - Example: `mybizz-core_2026-02-15`

#### Setup Instructions

**Create Backup Script:**
1. Create file: `C:\_Data\_Mybizz\scripts\daily_backup.bat`
```batch
@echo off
SET SOURCE=C:\path\to\mybizz-core
SET DEST=C:\_Data\_Mybizz\backup
SET TIMESTAMP=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
SET BACKUP_NAME=mybizz-core_%TIMESTAMP%

robocopy "%SOURCE%" "%DEST%\%BACKUP_NAME%" /MIR /R:3 /W:5 /LOG:"%DEST%\logs\backup_%TIMESTAMP%.log"

echo Backup completed: %BACKUP_NAME% >> "%DEST%\logs\backup_history.txt"
```

**Configure Windows Scheduled Task:**
1. Open Task Scheduler (taskschd.msc)
2. Create Basic Task → Name: "MyBizz Daily Backup"
3. Trigger: Daily at 17:00
4. Action: Start a program
5. Program: `C:\_Data\_Mybizz\scripts\daily_backup.bat`
6. Settings:
   - Run whether user is logged on or not
   - Run with highest privileges
   - If task fails, restart every 15 minutes, max 3 attempts

**Verify Scheduled Task:**
```batch
# Check task status
schtasks /query /tn "MyBizz Daily Backup" /fo LIST /v

# Run task manually to test
schtasks /run /tn "MyBizz Daily Backup"
```

#### Verification Procedure
```batch
# Check if today's backup exists
dir "C:\_Data\_Mybizz\backup\mybizz-core_*" /O-D

# Verify backup folder size (should be similar to repo size)
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15" /S

# Check backup log for errors
type "C:\_Data\_Mybizz\backup\logs\backup_2026-02-15.log"

# Quick test: Compare file count
dir "C:\path\to\mybizz-core" /S /B | find /c /v "" > count_source.txt
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15" /S /B | find /c /v "" > count_backup.txt
```

#### Restore Method
```batch
# Restore entire repo from specific date backup
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15" "C:\path\to\mybizz-core" /MIR /R:3 /W:5

# Restore specific folder only
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15\client_code" "C:\path\to\mybizz-core\client_code" /MIR /R:3 /W:5

# Restore single file
copy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15\client_code\contacts.py" "C:\path\to\mybizz-core\client_code\contacts.py"
```

#### Cleanup Procedure
- **Managed by:** User (manual)
- **Frequency:** Weekly or monthly
- **Retention Policy:** Keep 7-30 days of daily backups
- **Command:**
```batch
# Delete backups older than 30 days
forfiles /p "C:\_Data\_Mybizz\backup" /m "mybizz-core_*" /d -30 /c "cmd /c rd /s /q @path"

# Keep only last 7 backups
# (Manual: sort by date, delete oldest except last 7)
```

---

### Layer 4: Incidental Full Backups
- **Provider:** Continue.dev agent (user-initiated)
- **Retention:** 48 hours (automatic cleanup)
- **Location:** `C:\_Data\_Mybizz\backup\`
- **Use Case:** Milestone preservation, pre-refactor safety net
- **Limitations:** Disk space, requires manual trigger discipline
- **Advantage:** Captures specific development milestones
- **Trigger:** Manual, strategic moments:
  - After feature complete (milestone)
  - Before major refactoring (safety net)
  - After successful bug fix (verified solution)
  - After all tests passing (known good state)
  - Before integration tests (pre-risk checkpoint)
- **Content:** Complete local repo snapshot
- **Naming Convention:** `mybizz-core_YYYY-MM-DD_HH-MM_description`
  - Example: `mybizz-core_2026-02-01_14-30_contacts-feature-complete`
  - Example: `mybizz-core_2026-02-01_09-15_before-integration-tests`
  - Example: `mybizz-core_2026-01-31_16-45_milestone-bookings-complete`

#### Verification Procedure
```batch
# Verify backup was created
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_*" /O-D

# Compare folder sizes (backup should match source)
dir "C:\path\to\mybizz-core" /S
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_14-30_contacts-feature-complete" /S

# Quick integrity check: verify key files exist
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_14-30_contacts-feature-complete\client_code\*.py"
```

#### Restore Method
```batch
# Restore from specific milestone
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_14-30_contacts-feature-complete" "C:\path\to\mybizz-core" /MIR /R:3 /W:5

# Preview what would be restored (dry run)
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_14-30_contacts-feature-complete" "C:\path\to\mybizz-core" /MIR /L

# Restore specific folder from milestone
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_14-30_contacts-feature-complete\server_code" "C:\path\to\mybizz-core\server_code" /MIR /R:3 /W:5
```

#### Cleanup Procedure
- **Managed by:** Continue.dev agent (automatic)
- **Frequency:** Automatic after 48 hours
- **Retention Policy:** 
  - Delete all non-milestone backups older than 48 hours
  - Keep milestone backups (named with "milestone" in description) indefinitely
  - Safety net: Layer 3 daily backups preserve content beyond 48 hours
  - Additional safety: All successful tests followed by GitHub push
- **Command:**
```batch
# Automatic cleanup by Continue.dev (runs after 48 hours)
# Deletes: mybizz-core_<date>_* where date < (today - 2 days) AND description != "*milestone*"

# Manual cleanup if needed:
forfiles /p "C:\_Data\_Mybizz\backup" /m "mybizz-core_*" /d -2 /c "cmd /c if not @fname==*milestone* rd /s /q @path"
```

---

### Layer 5: Working Files Backup
- **Provider:** Continue.dev agent (user-initiated)
- **Retention:** Until current task tests successfully
- **Location:** `C:\path\to\mybizz-core\theme\assets\Backup_Temp\`
- **Use Case:** Temporary safety net during active editing
- **Limitations:** Only exists during feature development/refactoring
- **Advantage:** Instant rollback for current work-in-progress
- **Trigger:** Before high-risk operations:
  - Before major refactoring (safety net)
  - Before integration tests (Data Tables risk)
  - Before Data Tables schema changes (high risk)
  - Before Anvil Uplink operations with write access
- **Content:** Individual files currently being edited
- **Naming Convention:** `YYYY-MM-DD_HH-MM_filename_description`
  - Example: `2026-02-15_14-30_contacts.py_before-refactor`
  - Example: `2026-02-15_09-15_bookings_form.py_before-schema-change`
  - Example: `2026-02-15_11-45_reports_module.py_before-integration-test`

#### Verification Procedure
```batch
# Verify backup file was created
dir "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_*"

# Compare file size with original
dir "C:\path\to\mybizz-core\client_code\contacts.py"
dir "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor"

# Quick content check (verify not corrupted)
type "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor" | find "def " /c
```

#### Restore Method
```batch
# Restore single file from temp backup
copy "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor" "C:\path\to\mybizz-core\client_code\contacts.py" /Y

# Restore with confirmation
copy "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor" "C:\path\to\mybizz-core\client_code\contacts.py"

# Preview file before restoring
type "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor"
```

#### Cleanup Procedure
- **Managed by:** Continue.dev agent (automatic)
- **Trigger:** After current task tests successfully
- **Frequency:** Immediate upon successful test completion
- **Command:**
```batch
# Automatic cleanup by Continue.dev after successful tests
# Deletes all files in Backup_Temp for current task

# Manual cleanup if needed:
del "C:\path\to\mybizz-core\theme\assets\Backup_Temp\2026-02-15_14-30_contacts.py_before-refactor"

# Clear entire temp folder (use with caution)
del "C:\path\to\mybizz-core\theme\assets\Backup_Temp\*" /Q
```

---

## Emergency Recovery Quick Reference

### Accidental File Deletion (< 5 minutes ago)
→ **Check Layer 5:** Backup_Temp folder
```batch
dir "C:\path\to\mybizz-core\theme\assets\Backup_Temp\*" /O-D
copy "C:\path\to\mybizz-core\theme\assets\Backup_Temp\[latest-file]" "C:\path\to\[destination]"
```

### Bad Edit During Current Work Session
→ **Check Layer 5:** Backup_Temp folder for pre-refactor version
```batch
# List recent temp backups
dir "C:\path\to\mybizz-core\theme\assets\Backup_Temp\*" /O-D
# Restore desired file
copy "C:\path\to\mybizz-core\theme\assets\Backup_Temp\[file]" "[destination]"
```

### Need to Rollback Last Few Hours of Work
→ **Check Layer 4:** Incidental backups from today
```batch
dir "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15_*" /O-D
robocopy "[backup-path]" "C:\path\to\mybizz-core" /MIR /R:3 /W:5
```

### Need Yesterday's or Recent Day's Version
→ **Check Layer 3:** Auto scheduled daily backup
```batch
dir "C:\_Data\_Mybizz\backup\mybizz-core_*" /O-D
robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-14" "C:\path\to\mybizz-core" /MIR /R:3 /W:5
```

### Bad Commit Pushed to GitHub (< 48 hours)
→ **Check Layer 1:** Anvil History OR **Layer 2:** Git revert
```bash
# Anvil: Editor → Settings → History → Restore

# Git revert (safe, preserves history)
git revert <bad-commit-hash>
git push origin main

# Git reset (destructive, use with caution)
git reset --hard <good-commit-hash>
git push --force origin main
```

### Need Specific Feature Milestone
→ **Check Layer 4:** Search for milestone backup
```batch
dir "C:\_Data\_Mybizz\backup\*milestone*" /S /B
robocopy "[milestone-backup-path]" "C:\path\to\mybizz-core" /MIR /R:3 /W:5
```

### Complete Disaster (Local Repo Corrupted)
→ **Priority Order:**
1. **Layer 2:** Clone fresh from GitHub
   ```bash
   cd C:\path\to\projects
   git clone https://github.com/yourusername/mybizz-core.git mybizz-core-recovered
   ```
2. **Layer 3:** Restore from most recent daily backup
3. **Layer 1:** Pull from Anvil History if GitHub unavailable

---

## Integration with Development Workflow

### Standard Feature Implementation
1. **Plan feature** (write spec, identify files to modify)
2. **Backup (Layer 5)** - working files to Backup_Temp
3. **Backup (Layer 4)** - full repo before starting
4. Extract pure logic + write tests
5. **Backup (Layer 4)** - before integration tests
6. Run integration tests
7. **Verify all tests pass**
8. **Backup (Layer 4)** - milestone: feature complete
9. **Push to GitHub (Layer 2)**
10. **Cleanup (Layer 5)** - delete temp backups (Continue.dev automatic)

### Standard Bug Fix
1. **Reproduce bug + write test**
2. **Backup (Layer 5)** - affected files to Backup_Temp
3. Implement fix
4. **Verify all tests pass**
5. **Backup (Layer 4)** - after fix verified
6. **Push to GitHub (Layer 2)**
7. **Cleanup (Layer 5)** - delete temp backups (Continue.dev automatic)

### High-Risk Operations Checklist
Before any of these operations:
- [ ] **Layer 5 backup** of all affected files
- [ ] **Layer 4 backup** of entire repo
- [ ] Verify backups exist and are valid
- [ ] Document what you're about to change

**High-risk operations:**
- Data Tables schema changes
- Anvil Uplink operations with write access
- Major refactoring (>100 lines changed)
- Integration test runs that modify data
- Database migration scripts

---

## Backup Health Checklist (Weekly)

- [ ] **Layer 3:** Verify scheduled task ran yesterday (check backup folder)
- [ ] **Layer 3:** Test Task Scheduler status
  ```batch
  schtasks /query /tn "MyBizz Daily Backup" /fo LIST /v
  ```
- [ ] **Layer 4:** Review backup folder, verify milestones preserved
- [ ] **Layer 4:** Confirm 48-hour cleanup is working (no old non-milestone backups)
- [ ] **Layer 5:** Confirm Backup_Temp is empty or contains only active work
- [ ] **Layer 2:** Verify GitHub sync
  ```bash
  git status
  git log origin/main -5
  ```
- [ ] **Test restore:** Pick random backup, restore single file, verify integrity
- [ ] **Check disk space:** Backup folder size vs. allocation
  ```batch
  dir "C:\_Data\_Mybizz\backup" /S
  ```

---

## Disk Space Management

### Estimated Space Requirements
- **Per backup:** ~2-5 MB (typical mybizz-core repo size)
- **Layer 3:** 7-30 daily backups = 14-150 MB
- **Layer 4:** 5-10 milestone backups = 10-50 MB
- **Layer 5:** 2-5 temp files = <1 MB
- **Total allocation recommended:** 200-300 MB

### Cleanup Schedule
- **Layer 1:** Automatic (Anvil-managed)
- **Layer 2:** Automatic (GitHub-managed)
- **Layer 3:** Weekly/monthly manual cleanup (keep 7-30 days)
- **Layer 4:** Automatic after 48 hours (Continue.dev-managed)
- **Layer 5:** Automatic after tests pass (Continue.dev-managed)

### Storage Alert Thresholds
- **Warning:** Backup folder exceeds 250 MB
- **Critical:** Backup folder exceeds 500 MB
- **Action:** Review and delete old Layer 3 backups beyond retention policy

---

## Notes on Data Tables

- **Data Tables:** Stored on Anvil platform, NOT in local repo
- **Local Repo Contains:** Only Data Tables schema definitions
- **Schema Updates:** Received from GitHub when updating local repo
- **Data Backup:** Managed by Anvil.works (Layer 1)
- **Schema Backup:** Covered by all layers (part of repo)
- **High Risk:** Schema changes require Layer 5 backup before modification

---

**Last Updated:** 2026-02-15
**Next Review:** 2026-03-15
