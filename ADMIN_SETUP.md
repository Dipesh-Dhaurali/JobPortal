# Admin Panel Setup Guide

## Overview
The Admin Panel is a comprehensive management system for the JobPortal platform. It provides administrators with tools to manage users, moderate content, and monitor platform activities.

## Features

### 1. Admin Dashboard
- **Statistics Overview**: Display total users, HR accounts, candidates, and job posts
- **User Breakdown**: Active, suspended, and pending users
- **Recent Activities**: Track admin actions and system events
- **Quick Actions**: Direct links to manage users and moderate jobs

### 2. User Management
- **View All Users**: Browse HR accounts and candidates separately
- **Search & Filter**: Find users by username or email
- **User Profiles**: Access detailed HR and candidate profiles
- **Account Control**: Suspend or activate user accounts
- **Suspension Tracking**: Log reasons for account suspensions

### 3. Job Moderation
- **View All Jobs**: Browse all job postings across the platform
- **Search Jobs**: Find jobs by title or company name
- **Edit Jobs**: Modify job details (title, salary, employment type, etc.)
- **Delete Jobs**: Remove inappropriate or spam job listings
- **View HR Profiles**: Check company details and job posting history

### 4. Profile Management
- **HR Profiles**: View company information, contact details, and all posted jobs
- **Candidate Profiles**: Review candidate education, skills, work experience, and applications
- **Application Tracking**: See all job applications from each candidate

## Setup Instructions

### Step 1: Run Database Migrations
First, create the admin models in the database:

```bash
python manage.py makemigrations admin_portal
python manage.py migrate admin_portal
```

### Step 2: Create an Admin User
Use Django's shell to create an admin account:

```bash
python manage.py shell
```

Then in the Python shell:

```python
from django.contrib.auth.models import User
from admin_portal.models import AdminUser

# Create a superuser (if not already done)
admin_user = User.objects.create_user(
    username='admin',
    email='admin@jobportal.com',
    password='your_secure_password',
    is_staff=True,
    is_superuser=True
)

# Create AdminUser record
AdminUser.objects.create(user=admin_user, is_super_admin=True)

print("Admin user created successfully!")
```

### Step 3: Access the Admin Panel
1. Log in at `/login/` with your admin credentials
2. You'll be automatically redirected to `/admin/` (admin dashboard)
3. Or directly navigate to `http://localhost:8000/admin/`

## User Roles

### Admin
- Full access to admin panel
- Can manage users and moderate content
- Can view and edit all platform data

### HR/Company
- Can post and manage job listings
- Can view candidate applications
- Can shortlist and select candidates

### Candidate
- Can search and apply for jobs
- Can manage their profile and applications
- Can view job details and company profiles

## Admin URLs

| Endpoint | Purpose |
|----------|---------|
| `/admin/` | Admin Dashboard |
| `/admin/users/` | User Management |
| `/admin/users/<id>/suspend/` | Suspend User |
| `/admin/users/<id>/activate/` | Activate User |
| `/admin/jobs/` | Job Moderation |
| `/admin/jobs/<id>/edit/` | Edit Job Post |
| `/admin/jobs/<id>/delete/` | Delete Job Post |
| `/admin/hr-profile/<id>/` | View HR Profile |
| `/admin/candidate-profile/<id>/` | View Candidate Profile |

## Models

### AdminUser
Represents an administrator on the platform.

**Fields:**
- `user` - OneToOne link to Django User
- `is_super_admin` - Boolean flag for super admin status
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update

### UserStatus
Tracks the status of user accounts.

**Fields:**
- `user` - OneToOne link to Django User
- `user_type` - 'hr' or 'candidate'
- `status` - 'active', 'suspended', or 'pending'
- `reason_for_suspension` - Text reason for suspension
- `suspended_at` - Timestamp of suspension
- `suspended_by` - Admin who suspended the user

### JobPostModeration
Tracks moderation actions on job posts.

**Fields:**
- `job_post` - OneToOne link to JobPost
- `status` - 'flagged', 'approved', 'rejected', 'edited', or 'deleted'
- `reason` - Text reason for moderation action
- `moderated_by` - Admin who moderated the job
- `moderated_at` - Timestamp of moderation

### AdminActivityLog
Audit trail of all admin actions.

**Fields:**
- `admin` - ForeignKey to AdminUser
- `action_type` - Type of action performed
- `description` - Detailed description of action
- `target_user` - User affected by action
- `created_at` - Timestamp of action

## Important Notes

1. **Super Admins**: Only super admins can access the full admin panel
2. **Audit Trail**: All admin actions are logged in AdminActivityLog
3. **User Suspension**: Suspended users cannot log in but their accounts remain intact
4. **Data Integrity**: Deleting a job post will remove associated applications
5. **Security**: Admin decorators prevent unauthorized access to admin pages

## Security Best Practices

1. Use strong, unique passwords for admin accounts
2. Regularly review the activity log for suspicious actions
3. Suspend accounts that violate platform policies
4. Keep admin accounts secure and limit access
5. Regularly backup the database
6. Monitor job posts for spam or inappropriate content

## Troubleshooting

### Issue: Admin not redirected to dashboard after login
**Solution**: Ensure AdminUser record exists for the user. Check in Django shell:
```python
from admin_portal.models import AdminUser
AdminUser.objects.filter(user__username='admin_username').exists()
```

### Issue: Cannot access admin pages
**Solution**: Verify AdminUser record exists and user is properly authenticated. Check:
1. User is logged in
2. AdminUser relationship exists
3. Session is not expired

### Issue: User status not updating
**Solution**: Check that UserStatus model is properly created. Run migrations:
```bash
python manage.py migrate admin_portal
```

## Support
For issues or questions about the admin panel, contact the development team or refer to the Django admin documentation.
