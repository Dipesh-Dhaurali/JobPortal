# Job Portal - Technical Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Frontend Layer                     │
│  (HTML Templates + Bootstrap CSS + JavaScript)      │
└─────────────────────────────────────────────────────┘
                         ↓ HTTP Requests
┌─────────────────────────────────────────────────────┐
│              Django URL Router (urls.py)             │
│         Directs requests to appropriate views       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│              View Layer (views.py)                  │
│    Business Logic & Request Processing             │
│  - Authentication Views                            │
│  - Candidate Views                                 │
│  - HR Views                                        │
│  - Public Views                                    │
└─────────────────────────────────────────────────────┘
                         ↓ ORM Queries
┌─────────────────────────────────────────────────────┐
│            Django ORM (Object-Relational)           │
│     Models.py - Database Object Definitions         │
└─────────────────────────────────────────────────────┘
                         ↓ SQL Queries
┌─────────────────────────────────────────────────────┐
│           Database Layer (SQLite)                   │
│   Tables for Users, Jobs, Applications, etc.        │
└─────────────────────────────────────────────────────┘
```

---

## Project Structure

```
JobPortal/
│
├── jobportal/              # Main project folder
│   ├── settings.py        # Project configuration
│   ├── urls.py            # Main URL routing
│   ├── asgi.py            # ASGI config
│   ├── wsgi.py            # WSGI config
│   └── __init__.py
│
├── authuser/              # Authentication app
│   ├── models.py          # User & ContactMessage models
│   ├── views.py           # Auth views (login, register)
│   ├── urls.py            # Auth URLs
│   ├── admin.py           # Admin configurations
│   ├── forms.py           # Authentication forms
│   └── templates/
│       ├── loginUser.html
│       ├── candidateregister.html
│       └── hrregister.html
│
├── candidate/             # Candidate app
│   ├── models.py          # Candidate models (Profile, Education, Skills)
│   ├── views.py           # Candidate views (dashboard, profile, jobs)
│   ├── urls.py            # Candidate URLs
│   ├── admin.py           # Candidate admin
│   ├── forms.py           # Candidate forms
│   └── templates/
│       ├── dashboard.html
│       ├── profile.html
│       ├── job_detail.html
│       ├── applied_jobs.html
│       └── view_hr_profile.html
│
├── hr/                    # HR/Recruiter app
│   ├── models.py          # Company, Job, Application models
│   ├── views.py           # HR views (job posting, candidates)
│   ├── urls.py            # HR URLs
│   ├── admin.py           # HR admin
│   ├── forms.py           # HR forms
│   └── templates/
│       ├── hrdashboard.html
│       ├── postjob.html
│       ├── editjob.html
│       ├── candidates.html
│       ├── profile.html
│       ├── view_candidate_profile.html
│       └── job_history.html
│
├── static/                # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                 # User uploaded files
│   ├── profiles/          # Profile pictures
│   ├── resumes/           # Resume files
│   └── logos/             # Company logos
│
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── db.sqlite3            # SQLite database
```

---

## MTV Architecture (Model-Template-View)

### Model (models.py)
```python
# Database layer - Defines data structure
class User(AbstractUser):
    role = models.CharField(choices=ROLE_CHOICES)
    
class Job(models.Model):
    title = models.CharField()
    salary = models.CharField()
    # Fields mapped to database columns
```

**Responsibilities:**
- Define database schema
- Establish relationships (ForeignKey, ManyToMany, OneToOne)
- Implement validation logic
- Query methods for data retrieval

### Template (*.html)
```html
<!-- Presentation layer - Frontend rendering -->
{% extends 'base.html' %}
{% block content %}
    <h1>{{ job.title }}</h1>
    <p>{{ job.description }}</p>
{% endblock %}
```

**Responsibilities:**
- Display data to users
- Handle form rendering
- Control conditional content display
- Implement user interface

### View (views.py)
```python
# Business logic layer - Process requests
def job_detail(request, id):
    job = Job.objects.get(id=id)
    context = {'job': job}
    return render(request, 'job_detail.html', context)
```

**Responsibilities:**
- Handle HTTP requests
- Query models for data
- Process form submissions
- Return responses (HTML, redirects, JSON)
- Implement business logic

---

## Database Schema & Relationships

### Entity Relationship Diagram (Conceptual)

```
┌─────────────┐
│    User     │ (1)
│  (Custom    │────┐ (1)
│ AbstractUser)   │
└─────────────┘   │
      ↑           ├──→ ┌──────────────┐
      │           │    │  Candidate   │
      │ (1)       │    │   (Profile)  │
      │           │    └──────────────┘
      │           │           ↓
      │           │      (1-Many)
      │           │           ↓
      │           └──→ ┌──────────────────────┐
      │                │ CandidateEducation   │
      │                │ CandidateExperience  │
      │                │ CandidateSkill       │
      │                │ CandidateLanguage    │
      │                └──────────────────────┘
      │
      ├──→ ┌──────────────┐
      │    │   Company    │
      │    │ (HR Profile) │
      │    └──────────────┘
      │           ↓
      │      (1-Many)
      │           ↓
      │    ┌──────────────┐
      │    │     Job      │
      │    └──────────────┘
      │           ↓
      │      (1-Many)
      │           ↓
      │    ┌──────────────┐
      │    │ Application  │
      │    └──────────────┘
      │           ↓
      │      (1-Many)
      │           ↓
      │    ┌──────────────────┐
      │    │ApplicationStatus │
      │    └──────────────────┘
      │
      └──→ ┌──────────────────┐
           │  ContactMessage  │
           └──────────────────┘
```

### Foreign Key Relationships

```python
# Job belongs to Company (1-to-Many)
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

# Application connects Candidate to Job (Many-to-One both ways)
class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

# ApplicationStatus tracks history
class ApplicationStatus(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
```

### Many-to-Many Relationships

```python
# Candidate has multiple Skills, Skill belongs to multiple Candidates
class Candidate(models.Model):
    skills = models.ManyToManyField(CandidateSkill)
    
# Candidate has multiple Languages, Language belongs to multiple Candidates
class Candidate(models.Model):
    languages = models.ManyToManyField(CandidateLanguage)
```

---

## User Authentication Flow

### Registration Flow

```
Step 1: User selects role (Candidate/HR)
   ↓
Step 2: Form submission with data
   ↓
Step 3: Views.py receives POST request
   ↓
Step 4: Validation checks
   - Username uniqueness
   - Email uniqueness
   - Password strength
   - Form validation
   ↓
Step 5: User model creation with hashed password
   ↓
Step 6: Extended profile creation
   - Candidate: Create Candidate profile
   - HR: Create Company profile
   ↓
Step 7: Success message and redirect to login
```

### Login Flow

```
Step 1: Username/Email and Password form submission
   ↓
Step 2: Views.py receives POST request
   ↓
Step 3: Authenticate user against database
   - Retrieve User by username
   - Verify password hash (Django's PBKDF2)
   ↓
Step 4: Check authentication result
   ✓ Success: Create session
   ✗ Failure: Show error message
   ↓
Step 5: Django session management
   - Store user_id in session
   - Set session cookie (HttpOnly)
   ↓
Step 6: Redirect to role-based dashboard
   - Candidate → /candidate/
   - HR → /hr/
   - Admin → /admin/
```

### Session & Authorization

```python
# Request contains session ID in cookie
# Django middleware checks session
# request.user is populated with authenticated User

# Check authentication in views
if request.user.is_authenticated:
    # User is logged in
    if request.user.role == 'CANDIDATE':
        # Candidate-specific logic
    elif request.user.role == 'HR':
        # HR-specific logic
```

---

## Job Application Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. Candidate searches jobs                          │
│    - Accesses /candidate/                           │
│    - Views filterable job list                      │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 2. Candidate views job details                      │
│    - Accesses /job/<id>/                           │
│    - Sees full job description                      │
│    - Sees company profile                          │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 3. Candidate applies to job                         │
│    - Clicks "Apply" button                          │
│    - POST request to /apply/<id>/                   │
│    - Validation: Not already applied, job active    │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 4. Application created in database                  │
│    - Application record created                     │
│    - ApplicationStatus: "Applied" (initial)         │
│    - created_at timestamp recorded                  │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 5. HR views applications                            │
│    - HR logs in to /hr/                             │
│    - Accesses job applications list                 │
│    - Filters by job, candidate                      │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 6. HR reviews candidate profile                     │
│    - Clicks on candidate name                       │
│    - Views full candidate profile                   │
│    - Sees education, experience, skills            │
│    - Sees resume (if uploaded)                     │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 7. HR makes first decision (Shortlist - Stage 1)    │
│    - Mark is_shortlisted = True                     │
│    - Add notes to ApplicationStatus                 │
│    - Update status to "Shortlisted"                 │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 8. Candidate receives notification                  │
│    - Application status updated                     │
│    - Visible in /candidate/applied-jobs/            │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 9. HR makes final decision (Stage 2)                │
│    - Mark is_selected = True                        │
│    - Add final notes                                │
│    - Update status to "Selected"                    │
└─────────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────┐
│ 10. Candidate receives final notification           │
│     - Status shows "Selected"                       │
│     - Application process complete                  │
└─────────────────────────────────────────────────────┘
```

---

## Data Validation & Security

### Input Validation

```python
# Model level validation
class Candidate(models.Model):
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')]
    )

# Form level validation (forms.py)
class CandidateRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
        return email

# View level validation
def register_candidate(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            # Process registration
        else:
            # Return errors to template
```

### Security Measures

```python
# 1. CSRF Protection
{% csrf_token %}  # In every POST form

# 2. Password Hashing
from django.contrib.auth.hashers import make_password
# Django automatically hashes passwords using PBKDF2

# 3. SQL Injection Prevention
# ✓ Correct: Using ORM
users = User.objects.filter(username=username)

# ✗ Wrong: Raw SQL (vulnerable)
# cursor.execute(f"SELECT * FROM authuser_user WHERE username='{username}'")

# 4. XSS Protection
{{ variable }}  # Django auto-escapes HTML by default

# 5. Email Validation
email = models.EmailField()  # Built-in email validation

# 6. Login Required
@login_required
def protected_view(request):
    pass

# 7. Role-based Access Control
if request.user.role != 'CANDIDATE':
    return redirect('home')
```

---

## Template Inheritance

### Base Template Structure

```html
<!-- base.html - Main template -->
<!DOCTYPE html>
<html>
<head>
    {% block head %}
        <title>{% block title %}Job Portal{% endblock %}</title>
        {% block extra_css %}{% endblock %}
    {% endblock %}
</head>
<body>
    {% include 'navbar.html' %}
    
    <main class="container">
        {% block content %}
        {% endblock %}
    </main>
    
    {% include 'footer.html' %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Child Template Extension

```html
<!-- job_detail.html - Extends base -->
{% extends 'base.html' %}

{% block title %}{{ job.title }} - Job Portal{% endblock %}

{% block content %}
    <h1>{{ job.title }}</h1>
    <p>{{ job.description }}</p>
{% endblock %}
```

---

## Context Variables Flow

```python
# View passes data through context dict
def candidatedashboard(request):
    jobs = Job.objects.filter(is_active=True)
    applications = Application.objects.filter(
        candidate=request.user.candidate
    )
    
    context = {
        'jobs': jobs,           # Accessible as {{ jobs }} in template
        'applications': applications,  # Accessible as {{ applications }}
        'user': request.user,   # Accessible as {{ user }}
        'total_jobs': jobs.count()  # Accessible as {{ total_jobs }}
    }
    
    return render(request, 'candidate/dashboard.html', context)
```

```html
<!-- dashboard.html - Uses context variables -->
<h1>Hello, {{ user.first_name }}</h1>

Total applications: {{ applications|length }}
Total jobs available: {{ total_jobs }}

{% for job in jobs %}
    <div class="job-card">
        <h2>{{ job.title }}</h2>
        <p>{{ job.company.company_name }}</p>
    </div>
{% endfor %}
```

---

## Middleware & Signals

### Django Middleware Stack

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Flow:
# Request → SecurityMiddleware → SessionMiddleware → ... → View
# Response ← SecurityMiddleware ← SessionMiddleware ← ... ← View
```

### Custom Signals (Future Enhancement)

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Application)
def application_created(sender, instance, created, **kwargs):
    if created:
        # Send notification to HR
        notify_hr_about_application(instance)
        # Create initial ApplicationStatus
        ApplicationStatus.objects.create(
            application=instance,
            status='Applied'
        )
```

---

## Performance Optimization

### Database Query Optimization

```python
# Without optimization (N+1 problem)
jobs = Job.objects.all()
for job in jobs:
    print(job.company.company_name)  # Extra query per job!

# With optimization (select_related)
jobs = Job.objects.select_related('company').all()
for job in jobs:
    print(job.company.company_name)  # No extra queries!

# With many-to-many optimization (prefetch_related)
candidates = Candidate.objects.prefetch_related('skills').all()
for candidate in candidates:
    print(candidate.skills.all())  # Optimized query
```

### Caching Strategy

```python
from django.core.cache import cache

# Cache job list
jobs = cache.get('jobs_list')
if jobs is None:
    jobs = Job.objects.all()
    cache.set('jobs_list', jobs, 3600)  # Cache for 1 hour

# Cache specific job
cache.set(f'job_{id}', job, 3600)
job = cache.get(f'job_{id}')
```

### Pagination for Large Datasets

```python
from django.core.paginator import Paginator

def job_list(request):
    jobs = Job.objects.all()
    paginator = Paginator(jobs, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'page_obj': page_obj}
    return render(request, 'jobs.html', context)
```

---

## Deployment Architecture

### Production Stack
```
┌─────────────────────────────────────────┐
│      Web Server (Gunicorn/uWSGI)       │
│   Handles WSGI requests from Django     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      Reverse Proxy (Nginx/Apache)       │
│   Routes requests, serves static files   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   Django Application                    │
│   Business logic and data processing    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│   Database (PostgreSQL recommended)     │
│   Persistent data storage               │
└─────────────────────────────────────────┘
```

---

## Future Architecture Enhancements

1. **API Layer**: RESTful API using Django REST Framework
2. **Microservices**: Separate notification service, search service
3. **Real-time Features**: WebSocket for live notifications
4. **Caching Layer**: Redis for session and data caching
5. **Search**: Elasticsearch for advanced job search
6. **Message Queue**: Celery for async tasks
7. **CDN**: CloudFront/Cloudflare for static files
8. **Monitoring**: Prometheus & Grafana for system monitoring
9. **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
10. **Containerization**: Docker for deployment consistency
