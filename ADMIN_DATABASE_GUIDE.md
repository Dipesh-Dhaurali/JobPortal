# Admin Panel Database & Usage Guide

## Problem Statement
You noticed that the Admin Panel appears empty with no data to display. This guide explains why and how to populate test data.

## Why Is Everything Empty?

The Admin Panel is **fully functional and working correctly**. The issue is:
- **No users have been created yet** - The database has no HR accounts, candidates, or job posts
- **No applications submitted** - There are no candidate applications to manage
- **This is normal for a new project** - A fresh database starts empty

## Solution: Populate Test Data

### Quick Start (Recommended)

1. **Navigate to project root directory**
   ```bash
   cd /path/to/jobportal
   ```

2. **Run the population script**
   ```bash
   python populate_test_data.py
   ```

3. **Success! You'll see output like:**
   ```
   ============================================================
   JobPortal Test Data Population Script
   ============================================================
   Clearing existing data...
   ✓ Cleared existing test data
   
   Creating admin user...
   ✓ Admin user created: admin_user / admin123
   
   Creating HR users...
   ✓ HR user created: test_techcorp (TechCorp Solutions)
   ✓ HR user created: test_fintech (FinTech Innovations)
   ✓ HR user created: test_healthmd (HealthMD Inc)
   
   Creating candidate users...
   ✓ Candidate user created: test_john_doe
   ✓ Candidate user created: test_jane_smith
   ...
   ```

### What Gets Created?

The script automatically creates:

**1 Admin User:**
- Username: `admin_user`
- Password: `admin123`
- Email: `admin@jobportal.com`

**3 HR/Company Users:**
- `test_techcorp` (TechCorp Solutions) - Technology
- `test_fintech` (FinTech Innovations) - Finance
- `test_healthmd` (HealthMD Inc) - Healthcare

**5 Candidate Users:**
- `test_john_doe`
- `test_jane_smith`
- `test_mike_wilson`
- `test_sarah_johnson`
- `test_alex_brown`

**4 Job Postings:**
- Senior Python Developer (TechCorp)
- Junior Django Developer (TechCorp)
- Frontend React Developer (FinTech)
- Healthcare Data Analyst (HealthMD)

**12+ Applications:**
- Candidates apply for various jobs

**All users automatically marked as:**
- Status: Active
- Ready for admin management

## Admin Panel Access

### Login to Admin Panel

1. Go to your application login page
2. Use these credentials:
   ```
   Username: admin_user
   Password: admin123
   ```
3. You'll be automatically redirected to `/admin_panel/` dashboard

### Admin Panel Features Available

#### 1. Dashboard
Shows real-time statistics:
- Total HR accounts (3)
- Total Candidate accounts (5)
- Total job posts (4)
- Total applications (12+)
- User status breakdown (active, suspended, pending)
- Recent job posts
- Recent admin activity

#### 2. User Management
- View all 8 users (1 admin + 3 HR + 5 candidates)
- Search users by username or email
- Filter by role (HR/Candidate)
- Suspend/activate user accounts
- View user profiles

#### 3. Job Moderation
- View all 4 job posts
- Search jobs by title or company
- Edit job details
- Delete inappropriate jobs
- View company profile of job poster

#### 4. Profile Management
- Click "View Profile" on any HR to see:
  - Company details (industry, size, location)
  - Company website and social media
  - Posted jobs by this company
  - Applications received
  
- Click "View Profile" on any Candidate to see:
  - Personal profile info
  - Skills and languages
  - Education background
  - Job applications submitted
  - Current application status

## Test User Scenarios

### Test as Admin
1. Login with: `admin_user` / `admin123`
2. Try:
   - Suspend a candidate account
   - Edit a job posting
   - Review candidate profiles
   - Check dashboard statistics

### Test as HR User
1. Login with: `test_techcorp` / `hr123456`
2. You'll see your dashboard with:
   - Your 2 posted jobs
   - Applications to your jobs
   - Candidate profiles who applied

### Test as Candidate
1. Login with: `test_john_doe` / `candidate123`
2. You'll see:
   - Your 4 job applications
   - Application statuses (all pending)
   - Job details for applied positions

## Important Notes

### Database Persistence
- This test data **persists in the database** until you run the population script again (which clears old data first)
- The admin panel shows **real, actual database data**, not mock data
- Changes made in the admin panel are **permanent**

### Re-running the Script
If you want to reset and repopulate:
```bash
python populate_test_data.py
```
This will:
1. Clear all old test data (with username starting with `test_` or `admin_user`)
2. Create fresh test data
3. All passwords are reset to defaults

### Manual Data Creation
You can also create data manually through the UI:
1. Register new HR user at `/register_hr/`
2. Create job posts through HR dashboard
3. Register candidate at `/register_candidate/`
4. Apply for jobs through candidate dashboard

## Troubleshooting

### Script won't run
```bash
# Make sure you're in the right directory
cd /path/to/jobportal

# Make sure Django is accessible
python manage.py --version  # Should show Django version

# Run with more verbose output
python -u populate_test_data.py
```

### Still seeing empty data after running script
1. Clear your browser cache (Ctrl+Shift+Delete)
2. Logout and login again
3. Check that you're logged in as `admin_user`
4. Verify script ran without errors

### Want to clear everything and start fresh
```bash
python manage.py flush  # WARNING: Deletes ALL data
python manage.py migrate  # Recreate empty database
python populate_test_data.py  # Populate with test data
```

## Admin Panel Capabilities Summary

✓ View 8 total users (admin, HR, candidates)
✓ View 4 job posts across 3 companies
✓ View 12+ candidate applications
✓ Search and filter all data
✓ Suspend/activate user accounts
✓ Edit job posting details
✓ Delete inappropriate jobs
✓ View detailed user profiles
✓ Track admin activity logs
✓ Monitor application statuses

The Admin Panel is **fully functional and ready to manage real data**!
