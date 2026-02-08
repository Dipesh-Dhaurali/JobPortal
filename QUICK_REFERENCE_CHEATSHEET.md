# Job Portal - Quick Reference Cheatsheet

## APP STRUCTURE AT A GLANCE

| App | Purpose | Key Models |
|-----|---------|-----------|
| **authuser** | User registration, login, classification | UserProfile, ContactMessage |
| **candidate** | Job searching, applications, profiles | CandidateAccount, CandidateProfile, MyApplyJobList |
| **hr** | Job posting, recruitment, shortlisting | JobPost, RecruiterProfile, ShortlistedCandidate, SelectedCandidate |
| **jobportal** | Main project settings & URL routing | - |

---

## KEY MODELS SUMMARY

### UserProfile
- **Purpose**: Classify users (candidate/hr/admin)
- **Key Fields**: user_type, is_verified, phone_number
- **Relationship**: OneToOne with User

### CandidateAccount
- **Purpose**: Track candidate account status
- **Status Options**: active, suspended, pending, inactive
- **Usage**: Account management and suspension

### CandidateProfile
- **Purpose**: Detailed candidate info for job matching
- **Key Fields**: education_level, skills, languages, work_experience, preferred_job_level
- **Education Choices**: SEE, SLC, +2, Diploma, Bachelor, Masters

### JobPost
- **Purpose**: Job listings created by HR
- **Key Fields**: title, address, salaryLow, salaryHigh, lastDateToApply, employment_type, work_mode
- **Validation**: Max salary > Min salary, Deadline > Today

### candidateApplication
- **Purpose**: Job applications with status tracking
- **Status**: pending, shortlisted, selected, rejected
- **Fields**: user, job, resume, support_documents, education_level, yearOfExp

### ShortlistedCandidate
- **Purpose**: Track shortlisted applicants
- **Special**: notification_sent flag to notify candidates

### RecruiterProfile
- **Purpose**: Company/HR profile
- **Fields**: company_name, industry, employee_size, about_company, social media links

---

## COMMON DJANGO TEMPLATES

### URL Tag (Navigation)
```django
{% url 'view_name' %}              <!-- Generate URL from view name -->
<a href="{% url 'login_user' %}">Login</a>
```

### CSRF Token (Form Security)
```django
<form method="POST">
    {% csrf_token %}               <!-- Must include in all POST forms -->
</form>
```

### Conditional Rendering
```django
{% if user.is_authenticated %}
    <p>Welcome {{ user.username }}</p>
{% else %}
    <a href="{% url 'login_user' %}">Login</a>
{% endif %}
```

### Loops
```django
{% for job in jobs %}
    <h3>{{ job.title }}</h3>
{% empty %}
    <p>No jobs found</p>
{% endfor %}
```

### Messages Display
```django
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

### Static Files
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

### Template Filters
```django
{{ created_at|date:"Y-m-d" }}      <!-- Format date -->
{{ name|upper }}                   <!-- Convert to uppercase -->
{{ price|floatformat:2 }}          <!-- Round to 2 decimals -->
```

---

## ESSENTIAL DJANGO COMMANDS

### Setup
```bash
python manage.py migrate               # Apply database migrations
python manage.py createsuperuser       # Create admin account
```

### Running
```bash
python manage.py runserver             # Start dev server (port 8000)
python manage.py runserver 0.0.0.0:8080   # Start on custom port
```

### Database
```bash
python manage.py makemigrations        # Create migrations after model changes
python manage.py sqlmigrate app 0001   # See SQL for migration
python manage.py dbshell               # Open SQL shell
python manage.py flush                 # Clear all data (careful!)
```

### Admin Access
```
Navigate to: http://localhost:8000/admin/
Login with superuser credentials
```

---

## AUTHENTICATION FLOW

```
1. User Registration
   └─> Django User created → CandidateAccount/HR created

2. User Login
   └─> authenticate() → Check credentials
       └─> Check user_type
           ├─> If HR → redirect to hrdash
           └─> If Candidate → redirect to candidate_dashboard

3. Protected Views
   └─> @login_required(login_url='login_user')
       └─> Redirects to login if not authenticated
```

---

## RECRUITMENT WORKFLOW

```
1. HR Posts Job
   └─> JobPost created by HR user

2. Candidate Applies
   └─> candidateApplication created
   └─> status = 'pending'

3. HR Reviews Applications
   └─> View all applications for job
   └─> Can shortlist, reject, or select

4. Shortlisting
   └─> Application status → 'shortlisted'
   └─> ShortlistedCandidate record created
   └─> Candidate gets notification

5. Final Selection
   └─> Application status → 'selected'
   └─> SelectedCandidate record created

6. Rejection (any stage)
   └─> Application status → 'rejected'
```

---

## ORM QUERY EXAMPLES

### Retrieve
```python
job = JobPost.objects.get(id=1)              # Get single record
jobs = JobPost.objects.all()                 # Get all
jobs = JobPost.objects.filter(title='Developer')  # Filter
jobs = JobPost.objects.exclude(status='rejected') # Exclude
job = JobPost.objects.first()                # First record
count = JobPost.objects.count()              # Count
```

### Filter with Multiple Conditions
```python
jobs = JobPost.objects.filter(
    user=request.user
).filter(
    salaryLow__gte=50000
).filter(
    CompanyName__icontains='Google'
).order_by('-created_at')
```

### Query Methods
```python
obj.exists()                    # Check if exists
obj.values('title', 'salary')   # Get specific fields only
obj.distinct()                  # Remove duplicates
obj.count()                      # Count results
obj.order_by('-created_at')     # Sort by date (newest first)
obj.first()                      # Get first record
obj.last()                       # Get last record
```

### Relationships
```python
user.jobpost_set.all()          # Get all jobs by user (reverse)
job.user.username               # Get job creator's username
job.candidateapplication_set.all()  # Get all applications for job
```

---

## FORM VALIDATION PATTERN

```python
# In view
if request.method == 'POST':
    form = JobPostForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, "Success!")
        return redirect('view_name')
    else:
        # Form has errors, display them
        context['form'] = form
        return render(request, 'template.html', context)
else:
    form = JobPostForm()
```

---

## ADMIN CUSTOMIZATION PATTERNS

### List Display & Filtering
```python
@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'CompanyName', 'created_at')
    list_filter = ('created_at', 'employment_type')
    search_fields = ('title', 'CompanyName')
    readonly_fields = ('created_at', 'applycount')
    ordering = ('-created_at',)
```

### Custom Actions
```python
def delete_all_jobs(self, request, queryset):
    count = queryset.count()
    queryset.delete()
    self.message_user(request, f"Deleted {count} jobs")

actions = ['delete_all_jobs']
```

### Fieldsets (Form Organization)
```python
fieldsets = (
    ('Basic Info', {
        'fields': ('title', 'address', 'CompanyName')
    }),
    ('Advanced', {
        'fields': ('created_at',),
        'classes': ('collapse',)
    }),
)
```

---

## URL PATTERNS USED

### Authuser URLs
```python
path("candidate-register/", views.register_candidate, name='register_candidate')
path("hr-register/", views.register_hr, name='register_hr')
path("login/", views.login_user, name='login_user')
path("logout/", views.logoutuser, name='logout_user')
```

### Candidate URLs
```python
path("candidate-dashboard/", views.candidate_dashboard, name='candidate_dashboard')
path("job/<int:pk>/", views.job_detail, name='job_detail')
path("profile/", views.candidate_profile, name='candidate_profile')
path("applied-jobs/", views.applied_jobs, name='applied_jobs')
```

### HR URLs
```python
path("hrdash/", views.hrhome, name='hrdash')
path("postjob/", views.post_job, name='postjob')
path("edit-job/<int:pk>/", views.edit_job, name='edit_job')
path("delete-job/<int:pk>/", views.delete_job, name='delete_job')
```

### Admin
```
/admin/                          Main admin dashboard
/admin/authuser/userprofile/     User management
/admin/candidate/candidateprofile/   Candidate profiles
/admin/hr/jobpost/               Job posts
```

---

## DEPLOYMENT CHECKLIST

- [ ] Set DEBUG = False in settings.py
- [ ] Use strong SECRET_KEY (environment variable)
- [ ] Configure ALLOWED_HOSTS properly
- [ ] Use PostgreSQL or MySQL instead of SQLite
- [ ] Set up HTTPS/SSL
- [ ] Configure static files (collectstatic)
- [ ] Set up logging
- [ ] Configure email backend
- [ ] Add error monitoring (Sentry)
- [ ] Database backups automated
- [ ] Use Gunicorn/uWSGI + Nginx
- [ ] Environment variables for secrets
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Security headers set

---

## COMMON ERROR SOLUTIONS

| Error | Solution |
|-------|----------|
| `TemplateDoesNotExist` | Check template path in list_display or template directory |
| `ObjectDoesNotExist` | Use `get_object_or_404()` or `.first()` instead of `.get()` |
| `IntegrityError` | Ensure ForeignKey references exist and OneToOne uniqueness |
| `ValidationError` | Implement proper clean() method in model |
| `Page not found (404)` | Check URL patterns in urls.py and path names |
| `CSRF token missing` | Add `{% csrf_token %}` in POST forms |
| `Permission denied` | Check @login_required and object ownership |
| `TypeError: 'str' object is not callable` | Check template tag syntax, might be using wrong delimiter |

---

## KEY CONCEPTS AT A GLANCE

### MTV Pattern
- **Model**: Database structure (models.py)
- **Template**: HTML rendering (templates/)
- **View**: Business logic (views.py)

### QuerySet Methods
- Lazy: Filter doesn't execute until needed
- Chainable: Can combine multiple filters
- Cached: Results stored after first evaluation

### Decorators
- `@login_required`: Require authentication
- `@require_http_methods`: Restrict HTTP methods
- `@transaction.atomic`: Ensure atomic operations

### Context Variables
- Passed from view to template
- Available in template as `{{ variable_name }}`
- Can contain lists, dictionaries, objects

### ORM Advantages
- Write once, works on any database
- Prevents SQL injection
- Provides validation layer
- Enables code reusability

---

## UNIQUE PROJECT FEATURES TO MENTION

1. **Three-Role System** (Candidate, HR, Admin)
2. **Advanced Job Filtering** (8+ parameters)
3. **Two-Stage Shortlisting** (shortlist → select)
4. **Comprehensive Profiles** (Education, skills, experience)
5. **Application Status Tracking** (pending → shortlisted → selected/rejected)
6. **Company Profiles** (Branding and social links)
7. **Public Contact Form** (Lead generation)
8. **Admin Controls** (Account suspension, bulk operations)
9. **CSRF Protection** (Security-first design)
10. **Cascading Deletes** (Data integrity)

---

## EXAMINER QUESTIONS - QUICK ANSWERS

**Q: What framework is used?**
A: Django 5.2.3 with SQLite database

**Q: How many users can it support?**
A: Unlimited theoretically; depends on server. With proper caching and database optimization, can scale to millions

**Q: Is it secure?**
A: Yes - has password hashing, CSRF protection, SQL injection prevention, access control, session management

**Q: Can recruiters post jobs?**
A: Yes, HR users can create, edit, delete, and manage jobs. They can also shortlist and select candidates

**Q: How do candidates apply?**
A: They browse jobs with advanced filtering, then click apply and submit resume + documents

**Q: How is data protected?**
A: Django ORM prevents SQL injection, passwords are hashed, CSRF tokens protect forms, access control limits data visibility

**Q: What makes it different?**
A: Complete ecosystem with 3 roles, advanced filtering, shortlisting workflow, comprehensive profiles, company branding

**Q: Can it be deployed?**
A: Yes, follow production checklist. Needs PostgreSQL, Gunicorn, Nginx, proper security configuration

---

## FINAL REMINDERS

- Always use `{% csrf_token %}` in POST forms
- Always use `@login_required` for protected views
- Always validate at model AND form level
- Always use QuerySet ORM instead of raw SQL
- Always show meaningful error messages
- Always use proper HTTP status codes
- Always implement proper access control
- Always follow Django best practices
- Always write clean, readable code
- Always test thoroughly before deployment

---

**Remember: Explain concepts clearly, show practical examples, and be ready for technical deep dives!**
