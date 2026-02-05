# How to Fix the Circular Import Error

## Problem
You're getting this error:
```
ImportError: cannot import name 'CandidateProfile' from partially initialized module 'candidate.models'
```

This happens because Python has cached bytecode files that contain old/incorrect imports.

## Solution

### Step 1: Clean Python Cache (Windows)
Run this file in Command Prompt or PowerShell:
```
cleanup_and_migrate.bat
```

### Step 2: Clean Python Cache (Mac/Linux)
Run this file in Terminal:
```bash
chmod +x cleanup_and_migrate.sh
./cleanup_and_migrate.sh
```

### Step 3: Manual Cleanup (If Scripts Don't Work)

**On Windows:**
```powershell
# Delete all __pycache__ folders
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force

# Delete all .pyc files
Get-ChildItem -Path . -Include *.pyc -Recurse -Force | Remove-Item -Force

# Then run migrations
python manage.py makemigrations authuser
python manage.py makemigrations candidate
python manage.py makemigrations hr
python manage.py makemigrations admin_portal
python manage.py migrate
```

**On Mac/Linux:**
```bash
# Delete all __pycache__ folders
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Delete all .pyc files
find . -type f -name "*.pyc" -delete

# Then run migrations
python manage.py makemigrations authuser
python manage.py makemigrations candidate
python manage.py makemigrations hr
python manage.py makemigrations admin_portal
python manage.py migrate
```

## What Was Fixed
1. Removed unnecessary comment line from candidate/models.py
2. Created cleanup scripts to clear Python cache
3. All imports are now clean with no circular dependencies

## Result
After running the cleanup scripts and migrations:
- Admin will show "Job Application Tracker" instead of "My apply job lists"
- Admin will show "Shortlist Notification" instead of "Is shortlisteds"
- All data will display properly in Django admin
- No more import errors
