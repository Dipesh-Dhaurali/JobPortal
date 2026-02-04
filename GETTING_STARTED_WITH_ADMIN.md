# Getting Started with Admin Panel - Quick Start Guide

## TL;DR - 2 Step Setup

### Step 1: Run Test Data Script
```bash
python populate_test_data.py
```

### Step 2: Login with Admin Credentials
```
Username: admin_user
Password: admin123
URL: /admin_panel/
```

---

## Problem Solved

✓ **Empty database is normal** - Your database is empty because no users/jobs have been created yet
✓ **Admin panel is working** - The admin interface is fully functional and ready to display data
✓ **Solution provided** - Use the test data script to populate realistic sample data

---

## What Happens When You Run the Script?

The `populate_test_data.py` script creates:

| Type | Count | Details |
|------|-------|---------|
| Admin Users | 1 | Full access to admin panel |
| HR Companies | 3 | TechCorp, FinTech, HealthMD |
| Candidates | 5 | Job seekers with profiles |
| Job Posts | 4 | Across multiple companies |
| Applications | 12+ | Candidates applying for jobs |

---

## Admin Panel Features You Can Now Test

### 1. Dashboard Overview
- **Real Statistics**: Shows actual counts of users, jobs, applications
- **Recent Activity**: Displays latest job posts and admin actions
- **User Breakdown**: Active, suspended, and pending accounts
- **Quick Stats**: 3 HR companies, 5 candidates, 4 jobs, 12+ applications

### 2. User Management
- **View all users** with filters for HR vs Candidates
- **Search functionality** by username or email
- **Suspend accounts** - Disable user access
- **Activate accounts** - Restore suspended users
- **View profiles** - Click to see detailed user information

### 3. Job Moderation
- **Browse all jobs** across all HR companies
- **Search jobs** by title or company name
- **Edit details** - Update job requirements, salary, etc.
- **Delete jobs** - Remove inappropriate or duplicate postings
- **View company** - See profile of company that posted job

### 4. Profile Management
- **HR Profiles**: Company info, size, industry, website, social links
- **Candidate Profiles**: Skills, education, experience, documents
- **Application tracking**: See all applications and their status
- **Contact information**: View company and candidate details

---

## Test Scenarios to Try

### Scenario 1: Review Candidate Applications
1. Login as admin_user
2. Go to Dashboard → View Statistics
3. See "12+ Applications"
4. Go to User Management
5. Click on `test_john_doe` → View Profile
6. See their applications to jobs

### Scenario 2: Manage Job Posts
1. Go to Job Moderation
2. See 4 job posts from 3 companies
3. Click Edit on "Senior Python Developer"
4. Change salary to 130,000-170,000
5. Save changes
6. Verify changes persist on refresh

### Scenario 3: Suspend a User
1. Go to User Management
2. Find `test_fintech` HR user
3. Click Suspend User
4. Confirm suspension
5. User status changes to "Suspended"

### Scenario 4: Review Company Profile
1. Go to Job Moderation
2. Find a job post from TechCorp
3. Click "View Company Profile"
4. See company details, size, industry
5. View all jobs posted by this company

---

## URL Reference

| Feature | URL |
|---------|-----|
| Dashboard | `/admin_panel/` |
| User Management | `/admin_panel/users/` |
| Job Moderation | `/admin_panel/jobs/` |
| Suspend User | `/admin_panel/users/<id>/suspend/` |
| Activate User | `/admin_panel/users/<id>/activate/` |
| Edit Job | `/admin_panel/jobs/<id>/edit/` |
| Delete Job | `/admin_panel/jobs/<id>/delete/` |
| View HR Profile | `/admin_panel/hr-profile/<id>/` |
| View Candidate Profile | `/admin_panel/candidate-profile/<id>/` |

---

## Database Capabilities

### The Admin Panel CAN Display:
✓ All registered users (HR and Candidates)
✓ All job postings from any company
✓ All applications submitted by candidates
✓ Complete user and company profiles
✓ Real-time statistics and counts
✓ Activity logs and modifications
✓ User status (active/suspended)

### The Admin Panel WILL Display:
✓ Your data once you create it OR
✓ Test data from the population script

### Current Status:
- Database: **Empty** (no users/jobs created yet)
- Admin Panel: **Fully Functional** (working perfectly)
- Solution: **Ready** (run test data script)

---

## Common Questions

### Q: Why is everything empty?
**A:** The database starts empty. Use `python populate_test_data.py` to add test data.

### Q: Is the admin panel broken?
**A:** No, it's working perfectly. There's just no data to display yet. The views are designed to show data once it exists.

### Q: Will the admin panel work with my real data?
**A:** Yes! The admin panel works with both test data and real user-created data. Any users, jobs, or applications created through the normal app will immediately appear in the admin panel.

### Q: Can I delete the test data?
**A:** Yes, run `python populate_test_data.py` again to clear old data and repopulate. Or use `python manage.py flush` to delete everything.

### Q: How do I prevent test data from being visible to production?
**A:** Don't run the population script in production. Only use it for development/testing. Real users create data through the normal app interface.

---

## Next Steps

1. ✓ Run: `python populate_test_data.py`
2. ✓ Login with: `admin_user` / `admin123`
3. ✓ Explore the admin panel
4. ✓ Try each feature with test data
5. ✓ Test with real users/data in production

---

## Support

For detailed information, see:
- `ADMIN_DATABASE_GUIDE.md` - Complete database troubleshooting
- `README_ADMIN_PANEL.md` - Full admin panel documentation
- `ADMIN_IMPLEMENTATION_SUMMARY.md` - Technical implementation details

The Admin Panel is **production-ready** and fully functional! 🚀
