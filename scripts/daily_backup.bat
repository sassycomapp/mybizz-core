@echo off
REM Daily Backup Script for MyBizz
REM Run via Windows Task Scheduler at 17:00 daily

SET SOURCE=C:\_Data\_Mybizz\mybizz-core
SET DEST=C:\_Data\_Mybizz\backup
SET TIMESTAMP=%date:~-4,4%-%date:~-7,2%-%date:~-10,2%
SET BACKUP_NAME=mybizz-core_%TIMESTAMP%

REM Create backup directory if it doesn't exist
if not exist "%DEST%" mkdir "%DEST%"
if not exist "%DEST%\logs" mkdir "%DEST%\logs"

REM Perform backup using robocopy
robocopy "%SOURCE%" "%DEST%\%BACKUP_NAME%" /MIR /R:3 /W:5 /XD .git __pycache__ /LOG:"%DEST%\logs\backup_%TIMESTAMP%.log"

REM Log completion
echo Backup completed: %BACKUP_NAME% at %time% >> "%DEST%\logs\backup_history.txt"
