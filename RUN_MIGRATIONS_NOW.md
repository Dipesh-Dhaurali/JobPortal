# CIRCULAR IMPORT FIXED - RUN THESE COMMANDS NOW

## Problem Fixed
The circular import error between `candidate/models.py`, `admin_portal/models.py`, and `hr/models.py` has been resolved by removing the unused `CandidateProfile` import from admin_portal/models.py.

## Commands to Run (In Order)

Open your terminal in the project directory and run these commands:

```bash
# Create migrations for authuser
python manage.py makemigrations authuser

# Create migrations for candidate
python manage.py makemigrations candidate

# Create migrations for hr
python manage.py makemigrations hr

# Create migrations for admin_portal
python manage.py makemigrations admin_portal

# Apply all migrations to the database
python manage.py migrate

# Restart your development server
python manage.py runserver
```

## What This Does
- Creates migration files for all the model changes we made (verbose_name additions, new fields)
- Applies those migrations to update your database schema
- Restarts your development server with the changes loaded

## After Migrations Complete
Go to Django admin (`/admin/`) and you should see:
- ✓ Renames working: "Job Application Tracker", "Shortlist Notification", "User Account Status", etc.
- ✓ Data showing: All models displaying properly
- ✓ No errors: Clean Django admin interface

## If You Get an Error
If you still get an import error, check:
1. No file is importing from `candidate.models` during Django startup
2. All imports are at the top of view/admin files (not in model definitions)
3. No circular references in model ForeignKey relationships
