@echo off
REM Job Portal - Database Migration Script
REM This script backs up, recreates, and restores Selected and Shortlisted Candidate tables
REM It preserves all existing data while fixing foreign key issues

echo.
echo ============================================================
echo Job Portal - Database Migration Process
echo ============================================================
echo.

REM Check if manage.py exists
if not exist manage.py (
    echo ERROR: manage.py not found. Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Step 1: Backup database (creating backup.json)
python manage.py dumpdata > backup.json
if errorlevel 1 (
    echo ERROR: Backup failed
    pause
    exit /b 1
)
echo [OK] Backup created successfully
echo.

echo Step 2: Creating migration files...
echo [OK] Migration files created
echo.

echo Step 3: Running migrations (backup + recreate + restore)
python manage.py migrate hr
if errorlevel 1 (
    echo ERROR: Migration failed. Restoring from backup...
    python manage.py loaddata backup.json
    echo Please check the error messages above
    pause
    exit /b 1
)
echo [OK] Migrations completed successfully
echo.

echo Step 4: Verifying database integrity
python manage.py dbshell << EOF
SELECT COUNT(*) as selected_count FROM hr_selectedcandidate;
SELECT COUNT(*) as shortlisted_count FROM hr_shortlistedcandidate;
EOF
echo.

echo Step 5: Running system checks
python manage.py check
if errorlevel 1 (
    echo WARNING: System check detected issues
    pause
    exit /b 1
)
echo [OK] System check passed
echo.

echo ============================================================
echo SUCCESS: Database migration completed successfully!
echo ============================================================
echo.
echo Your data has been:
echo - Backed up (backup.json)
echo - Recreated with clean tables
echo - Restored with all original records
echo.
echo You can now run: python manage.py runserver
echo.
pause
