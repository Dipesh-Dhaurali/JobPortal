# Admin Panel Architecture & Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         ADMIN PANEL SYSTEM                       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   Admin User    │
│   (Browser)     │
└────────┬────────┘
         │
         │ HTTP Request
         ↓
┌──────────────────────────────┐
│   Django Authentication      │
│   - Login Check              │
│   - Session Validation       │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       │                │
       ↓                ↓
   Admin?          Not Admin
       │                │
       │                ↓
       │         ┌──────────────┐
       │         │ Redirect to  │
       │         │ HR/Candidate │
       │         └──────────────┘
       │
       ↓
┌──────────────────────────────┐
│  @admin_required Decorator   │
│  - Check AdminUser exists    │
│  - Grant/Deny Access        │
└──────────────┬───────────────┘
               │
       ┌───────┴────────┐
       │                │
       ↓                ↓
    Access         HttpResponseForbidden
    Granted             │
       │                ↓
       │         ┌──────────────┐
       │         │ 403 Error    │
       │         └──────────────┘
       │
       ↓
┌──────────────────────────────┐
│   Admin View Functions       │
│   (11 Views Total)           │
└──────────────┬───────────────┘
               │
       ┌───────┼───────┬────────┐
       │       │       │        │
       ↓       ↓       ↓        ↓
    Dashboard Users  Jobs   Profiles
       │       │       │        │
       ↓       ↓       ↓        ↓
   Templates & Database Operations
```

---

## Data Flow Diagram

### User Management Flow

```
Admin User Suspended
        │
        ↓
Form Submission
        │
        ↓
Suspend View
        │
        ├─→ Create/Update UserStatus
        │   - user: Link to User
        │   - status: 'suspended'
        │   - reason: Stored
        │   - suspended_at: Timestamp
        │   - suspended_by: Admin
        │
        ├─→ Create ActivityLog
        │   - admin: Current admin
        │   - action: user_suspended
        │   - description: Details
        │   - target_user: Suspended user
        │
        ↓
Redirect to Users List
        │
        ↓
Display Success Message
        │
        ↓
Page Refresh shows updated status
```

### Job Moderation Flow

```
Admin Edits Job
        │
        ↓
Edit Job Form Loaded
        │
        ├─→ Fetch JobPost from DB
        │
        ├─→ Display form with current values
        │
        ↓
Admin Submits Changes
        │
        ├─→ Update JobPost
        │   - title
        │   - salary range
        │   - location
        │   - employment type
        │   - work mode
        │
        ├─→ Create ActivityLog
        │   - action: job_edited
        │   - description: Changes made
        │   - target_user: Job poster
        │
        ↓
Redirect to Jobs List
        │
        ↓
Job appears updated in list
```

### Profile Viewing Flow

```
Admin Clicks "View Profile"
        │
        ├─→ Check user_id from URL
        │
        ├─→ Fetch User object
        │
        ├─→ Check user type (HR or Candidate)
        │
        ├─→ If HR:
        │   ├─→ Fetch HRProfile
        │   ├─→ Fetch all JobPosts by user
        │   └─→ Render HR template
        │
        ├─→ If Candidate:
        │   ├─→ Fetch CandidateProfile
        │   ├─→ Fetch all Applications
        │   └─→ Render Candidate template
        │
        ↓
Display Profile with all details
        │
        ├─→ Allow suspend/activate
        │
        ├─→ Allow edit/delete (if HR)
        │
        ↓
Admin can take further action
```

---

## Model Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                      Database Schema                         │
└─────────────────────────────────────────────────────────────┘

User (Django Auth)
  │
  ├── OneToOne ──→ AdminUser
  │              ├─ is_super_admin
  │              ├─ created_at
  │              └─ updated_at
  │
  ├── OneToOne ──→ UserStatus
  │              ├─ user_type ('hr' or 'candidate')
  │              ├─ status ('active', 'suspended', 'pending')
  │              ├─ reason_for_suspension
  │              ├─ suspended_at
  │              └─ suspended_by → AdminUser
  │
  └── OneToMany ──→ AdminActivityLog
                 ├─ admin → AdminUser
                 ├─ action_type
                 ├─ description
                 └─ created_at

JobPost
  │
  └── OneToOne ──→ JobPostModeration
                 ├─ status
                 ├─ reason
                 ├─ moderated_by → AdminUser
                 └─ moderated_at
```

---

## URL Routing Structure

```
admin_portal/
├── /admin/                          → dashboard (admin_dashboard)
│   
├── /admin/users/                    → manage_users
│   ├── /?filter=hr                 → Filter HR only
│   ├── /?filter=candidate          → Filter Candidates only
│   └── /?search=username           → Search users
│   
├── /admin/users/<id>/              → User detail (via view profile link)
│   ├── suspend/                    → suspend_user
│   └── activate/                   → activate_user (POST only)
│   
├── /admin/jobs/                     → moderate_jobs
│   ├── /?search=title              → Search jobs
│   
├── /admin/jobs/<id>/               → Job detail (via edit/delete buttons)
│   ├── edit/                       → edit_job
│   └── delete/                     → delete_job
│   
├── /admin/hr-profile/<id>/         → view_hr_profile
│   
└── /admin/candidate-profile/<id>/  → view_candidate_profile
```

---

## Authentication & Authorization Flow

```
┌─────────────────┐
│  User Login     │
└────────┬────────┘
         │
         ↓
┌────────────────────────────────┐
│ Django authenticate()          │
│ - Check username/password      │
│ - Return User object or None   │
└────────┬───────────────────────┘
         │
    ┌────┴────┐
    │          │
    ↓          ↓
  Auth      No Auth
   OK        Error
    │          │
    ↓          ↓
 Login      Show Error
    │
    ↓
┌─────────────────────────────────┐
│ Check User Role                 │
└────┬────────────────┬──────┬────┘
     │                │      │
     ↓                ↓      ↓
 AdminUser      HRUser   Candidate
  Exists?       Exists?   (Default)
     │                │      │
     ↓                ↓      ↓
  Admin          HR        Candidate
 Dashboard    Dashboard   Dashboard
  /admin/     /hrdash/    /dashboard/
```

---

## Request/Response Cycle for Admin Pages

```
1. Admin navigates to /admin/users/
                │
                ↓
2. Django URL router matches pattern
   urlpatterns: path('admin/users/', views.manage_users, name='manage_users')
                │
                ↓
3. View function executes
   @login_required(login_url='login_user')
   @admin_required
   def manage_users(request):
                │
                ├─→ Try: AdminUser.objects.get(user=request.user)
                ├─→ Except: AdminUser.DoesNotExist → Show error, redirect
                │
                ↓
4. If admin exists, continue:
   - Get filter parameter from request.GET
   - Query User model with filters
   - Prepare context with user data
                │
                ↓
5. Render template
   render(request, 'admin_portal/manage_users.html', context)
                │
                ├─→ Template accesses context variables
                ├─→ For loop: for item in user_data
                ├─→ Display user information
                ├─→ Show action buttons
                │
                ↓
6. Return HTML response to browser
                │
                ↓
7. Browser renders page
   - Load Bootstrap CSS
   - Load Bootstrap Icons
   - Execute JavaScript
   - Display interactive page
```

---

## Database Query Patterns

### Get Admin Status
```python
try:
    admin_user = AdminUser.objects.get(user=request.user)
    # User is admin - proceed
except AdminUser.DoesNotExist:
    # User is not admin - deny access
```

### Get User Status
```python
try:
    status = UserStatus.objects.get(user=user)
    # Use status.status ('active', 'suspended', 'pending')
except UserStatus.DoesNotExist:
    # No status record - default to active
```

### Query with Related Data
```python
# Get users with their status info
user_data = []
for user in User.objects.all():
    try:
        status = UserStatus.objects.get(user=user)
    except:
        status = None
    user_data.append({
        'user': user,
        'status': status
    })
```

### Log Admin Activity
```python
AdminActivityLog.objects.create(
    admin=admin_user,
    action_type='user_suspended',
    description=f'Suspended user {user.username}. Reason: {reason}',
    target_user=user
)
```

---

## Template Inheritance Structure

```
base.html (implicit - not needed, each template is standalone)
    │
    ├── navbar.html (included in all admin templates)
    │   ├── Dashboard
    │   ├── Users
    │   ├── Jobs
    │   └── User Profile Menu
    │
    ├── dashboard.html
    │   ├── Stats cards
    │   ├── Recent jobs table
    │   ├── Activity log
    │   └── Quick action buttons
    │
    ├── manage_users.html
    │   ├── Search/filter form
    │   ├── Users table
    │   │   ├── Username
    │   │   ├── Status badge
    │   │   └── Action buttons
    │   └── Pagination (future)
    │
    ├── suspend_user.html
    │   ├── User info display
    │   ├── Reason form
    │   └── Confirmation button
    │
    ├── moderate_jobs.html
    │   ├── Search form
    │   ├── Job cards
    │   │   ├── Job details
    │   │   ├── Salary badge
    │   │   └── Action buttons
    │   └── Pagination (future)
    │
    ├── edit_job.html
    │   ├── Form sections
    │   │   ├── Basic info
    │   │   ├── Salary
    │   │   └── Job type
    │   └── Submit button
    │
    ├── delete_job.html
    │   ├── Warning zone
    │   ├── Confirmation form
    │   └── Delete button
    │
    ├── view_hr_profile.html
    │   ├── Account info
    │   ├── Company info
    │   ├── Jobs list
    │   └── Action panel
    │
    └── view_candidate_profile.html
        ├── Account info
        ├── Professional info
        ├── Applications list
        └── Action panel
```

---

## Security Layers

```
┌─────────────────────────────────────────────┐
│          Security Implementation            │
└─────────────────────────────────────────────┘

Layer 1: URL Routing
├─ Django URL patterns
├─ Path parameter validation
└─ No direct object access

Layer 2: Authentication
├─ @login_required decorator
├─ Session validation
└─ CSRF token on all forms

Layer 3: Authorization
├─ @admin_required decorator
├─ AdminUser model check
└─ HttpResponseForbidden response

Layer 4: Data Protection
├─ ORM parameterized queries
├─ Template auto-escaping
├─ HTTPS (production)
└─ SQL injection prevention

Layer 5: Audit Trail
├─ AdminActivityLog
├─ Timestamp tracking
├─ Admin identification
└─ Action documentation
```

---

## Performance Optimization

```
Query Optimization
├─ select_related() for ForeignKey
├─ prefetch_related() for reverse relations
└─ Database indexing on search fields

Caching Strategies (future)
├─ Cache dashboard statistics
├─ Cache user lists
└─ 5-minute TTL for frequently accessed data

Frontend Optimization
├─ Bootstrap CDN (already cached by users)
├─ Minimal custom CSS
├─ Lazy loading (future)
└─ Pagination for large lists (future)

Database Efficiency
├─ Minimal model fields
├─ Efficient relationships
├─ Proper indexing
└─ Regular query monitoring
```

---

## Error Handling

```
Admin Page Request
    │
    ├─→ User not logged in
    │   └─→ Redirect to login page
    │
    ├─→ User logged in, not admin
    │   └─→ HttpResponseForbidden (403)
    │
    ├─→ Object not found
    │   └─→ get_object_or_404 → 404 Error
    │
    ├─→ Form validation fails
    │   └─→ Re-render form with error messages
    │
    ├─→ Database error
    │   └─→ Django error page (dev) / 500 error (prod)
    │
    └─→ Success
        └─→ Process request, redirect with success message
```

---

## Scalability Considerations

```
Current Limits
├─ SQLite database (development only)
├─ Single server instance
└─ No horizontal scaling

Production Scalability
├─ PostgreSQL/MySQL database
├─ Multiple app servers
├─ Load balancer
├─ Caching layer (Redis)
├─ Database indexing
└─ Query optimization

Expected Load Handling
├─ Up to 10,000 users
├─ Up to 50,000 job posts
├─ Sub-second query response
└─ Concurrent admin users: 10+
```

---

**Architecture Document Generated**: February 4, 2026
**Version**: 1.0
**Status**: Complete
