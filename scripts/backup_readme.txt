MyBizz Backup Folder
====================

This folder contains automatic daily backups of the mybizz-core repository.

Backup Schedule:
- Daily at 5:00 PM via Windows Task Scheduler
- Retention: 7-30 days (manual cleanup required)

Backup Naming:
- Format: mybizz-core_YYYY-MM-DD
- Example: mybizz-core_2026-02-15

Logs:
- Location: backup\logs\
- Format: backup_YYYY-MM-DD.log

To Restore:
1. Find the backup folder with the date you need
2. Use robocopy to restore:
   robocopy "C:\_Data\_Mybizz\backup\mybizz-core_2026-02-15" "C:\_Data\_Mybizz\mybizz-core" /MIR /R:3 /W:5

For complete backup strategy, see:
theme\assets\System_Methods\ide_cop_backup.md

---
NOTE: Move this file to C:\_Data\_Mybizz\backup\README.txt
