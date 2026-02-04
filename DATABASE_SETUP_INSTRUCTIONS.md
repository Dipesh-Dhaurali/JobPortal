# JobPortal Database Setup Instructions

## Overview

This document provides complete instructions for setting up and initializing the JobPortal database with all necessary models and test data.

## Prerequisites

- Python 3.8+
- Django 5.2.3+
- SQLite (included with Django)
- All requirements from `requirements.txt` installed

## Step 1: Make Migrations for New Models

Run migrations for the authuser app that includes the new UserProfile model:

```bash
python manage.py makemigrations authuser
```

Run migrations for the admin_portal app:

```bash
python manage.py makemigrations admin_portal
```

## Step 2: Apply Migrations to Database

Apply all pending migrations:

```bash
python manage.py migrate
```

This creates all necessary database tables.

## Step 3: Initialize Database with Test Data

Run the database initialization script:

```bash
python manage_db.py
```

This script will:
- Create 1 Admin user
- Create 3 HR/Company accounts with complete profiles
- Create 5 Candidate accounts with detailed profiles
- Create 4 Job postings across different companies
- Create 12+ job applications
- Create shortlist notifications

## Complete Setup (One Command)

Run the automated setup script (Linux/Mac only):

```bash
chmod +x init_database.sh
./init_database.sh
```

For Windows, run commands individually in Command Prompt or PowerShell.

## Test Credentials

After successful setup, use these credentials to test the system:

### Admin Login
- **Username:** `admin_user`
- **Password:** `admin123`
- **URL:** `http://localhost:8000/admin_panel/`

### HR/Company Login
- **Username:** `tech_company_hr`
- **Password:** `hr@123456`
- **Company:** TechCorp Solutions

- **Username:** `finance_company_hr`
- **Password:** `hr@123456`
- **Company:** FinancePro Services

- **Username:** `health_company_hr`
- **Password:** `hr@123456`
- **Company:** HealthSystem Ltd

### Candidate Login
- **Username:** `john_candidate`
- **Password:** `candidate@123456`
- **Position:** Senior Software Engineer

- **Username:** `sarah_designer`
- **Password:** `candidate@123456`
- **Position:** UI/UX Designer

- **Username:** `alex_marketer`
- **Password:** `candidate@123456`
- **Position:** Digital Marketing Manager

- **Username:** `emma_developer`
- **Password:** `candidate@123456`
- **Position:** Full Stack Developer

- **Username:** `michael_analyst`
- **Password:** `candidate@123456`
- **Position:** Data Analyst

## Database Structure

### Core Models Created

**authuser app:**
- `UserProfile` - Extended user profile with user_type

**admin_portal app:**
- `AdminUser` - Admin user management
- `UserStatus` - User suspension/activation tracking
- `JobPostModeration` - Job post moderation audit
- `AdminActivityLog` - Admin action logging

**hr app (Enhanced):**
- `hr` - HR/Company basic model
- `HRProfile` - Complete company profile
- `JobPost` - Job postings
- `candidateApplication` - Job applications
- `ShortlistedCandidate` - Shortlist tracking
- `SelectedCandidate` - Final selection tracking

**candidate app (Enhanced):**
- `CandidateProfile` - Complete candidate profile
- `MyApplyJobList` - Applied jobs tracking
- `IsShortlisted` - Shortlist notifications

## Test Data Included

### Companies Created
1. **TechCorp Solutions** (Technology/Startup)
   - 51-200 employees
   - Jobs: Senior Python Developer, React Frontend Developer

2. **FinancePro Services** (Finance/Private)
   - 201-500 employees
   - Jobs: Financial Analyst

3. **HealthSystem Ltd** (Healthcare/Private)
   - 501-1000 employees
   - Jobs: Healthcare Administrator

### Candidates Created
1. John Doe - Software Engineer (3 years experience)
2. Sarah Williams - UI/UX Designer (5 years experience)
3. Alex Brown - Digital Marketing Manager (2 years experience)
4. Emma Davis - Full Stack Developer (1 year experience)
5. Michael Garcia - Data Analyst (4 years experience)

### Job Postings (4 total)
- All with salary ranges
- Different employment types (full-time, internship)
- Various work modes (remote, on-site, hybrid)
- 30-day application windows

### Applications (12+ total)
- All candidates have applied to relevant jobs
- Various application statuses
- Some candidates shortlisted for interviews

## Troubleshooting

### Migration Errors

**Error: "No changes detected"**
- Run: `python manage.py makemigrations --empty authuser --name fix_models`
- Edit the created migration file to include your model changes
- Run: `python manage.py migrate`

**Error: "Dependency on app 'X' before migration 'Y'"**
- Delete `admin_portal/migrations/` except `__init__.py`
- Run: `python manage.py migrate admin_portal zero`
- Re-run migrations

### Database Reset

To completely reset the database:

```bash
# Delete the database file
rm db.sqlite3

# Recreate migrations
rm authuser/migrations/00*.py
rm admin_portal/migrations/00*.py

# Run full setup again
python manage.py makemigrations authuser
python manage.py makemigrations admin_portal
python manage.py migrate
python manage_db.py
```

### Duplicate Data Error

If you get duplicate data errors when running `manage_db.py`:

```bash
# Clear all data first
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all().delete()
>>> exit()

# Then run the initialization script again
python manage_db.py
```

## Verify Setup

To verify all data was created correctly:

```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()  # Should be 9 (1 admin + 3 HR + 5 candidates)
>>> from hr.models import JobPost
>>> JobPost.objects.count()  # Should be 4
>>> from hr.models import candidateApplication
>>> candidateApplication.objects.count()  # Should be 12+
```

## Next Steps

1. Start the development server: `python manage.py runserver`
2. Log in with admin credentials
3. Navigate to `/admin_panel/` to access admin dashboard
4. Test HR functionality at `/hrdash/`
5. Test Candidate functionality at `/candidate_dashboard/`

## Support

If you encounter any issues:

1. Check the error message carefully
2. Verify Python and Django versions
3. Ensure all files are in correct locations
4. Run migrations individually to identify the problem
5. Check the troubleshooting section above

---

**Status:** Database setup is production-ready with comprehensive test data included.
