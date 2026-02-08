# Job Portal - Django Web Application

## Project Overview

Job Portal is a comprehensive recruitment platform built with Django that connects job seekers (candidates) with employers (HR/Recruiters). The platform enables companies to post job openings and candidates to search, apply, and track their applications.

### Project Type
- **Framework**: Django 5.2.3
- **Database**: SQLite
- **Python Version**: 3.8+
- **Frontend**: HTML, CSS, Bootstrap

---

## Features Overview

### For Candidates
- User registration and profile management
- Search jobs with advanced filtering (keyword, location, salary, employment type, work mode)
- Apply to jobs with single click
- Track application status
- View company profiles
- Manage profile with education, skills, languages, and experience
- Receive notifications on shortlisting
- Browse company information

### For HR/Recruiters
- Post and manage job openings
- Search and filter candidates
- View candidate profiles and applications
- Shortlist candidates in two stages
- Manage company profile and showcase company details
- Track applicants and their status
- Bulk operations for managing applications

### For Admin
- Full control over all users (candidates, HR, admins)
- Suspend/activate user accounts
- Manage all job postings
- Monitor contact messages
- View application status
- Bulk actions for data management

---

## Project Architecture

### Apps Structure

```
jobportal/
├── authuser/          # Authentication & User Management
├── candidate/         # Candidate Features & Dashboard
├── hr/               # HR/Recruiter Features & Job Management
└── jobportal/        # Main Project Settings
```

### Database Models (11 Models)

1. **User** - Custom user model with role-based access
2. **Candidate** - Extended candidate profile
3. **CandidateEducation** - Educational background
4. **CandidateSkill** - Skills tracking
5. **CandidateLanguage** - Language proficiency
6. **CandidateExperience** - Work experience
7. **Company** - Recruiter/HR company information
8. **Job** - Job postings
9. **Application** - Job applications
10. **ApplicationStatus** - Application status tracking
11. **ContactMessage** - Public contact form messages

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Dipesh-Dhaurali/JobPortal.git
cd JobPortal
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations**
```bash
python manage.py migrate
```

5. **Create a superuser (Admin)**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Main Portal: http://localhost:8000/
- Django Admin: http://localhost:8000/admin/

---

## User Roles & Access Control

### 1. Candidate (Job Seeker)
- **Registration**: Candidate registration page
- **Dashboard**: View applications, profile
- **Features**: 
  - Search jobs with advanced filters
  - Apply to jobs
  - View company profiles
  - Track application status
  - Manage profile information
- **URL Prefix**: `/candidate/`

### 2. HR/Recruiter
- **Registration**: HR registration page
- **Dashboard**: Job management, applicant tracking
- **Features**:
  - Post new jobs
  - Manage job postings
  - View applicant list
  - Shortlist candidates
  - View candidate profiles
  - Manage company profile
- **URL Prefix**: `/hr/`

### 3. Admin
- **Access**: Django Admin Panel (/admin/)
- **Features**:
  - Full data management
  - User account control
  - Bulk operations
  - System monitoring
  - Contact message management

---

## Key URLs & Endpoints

### Authentication Routes
```
/login/                    - User login
/register/                 - Registration page
/candidate-register/       - Candidate registration
/hr-register/              - HR registration
/logout/                   - Logout
```

### Candidate Routes
```
/candidate/                - Candidate dashboard
/candidate/profile/        - View/edit profile
/candidate/applied-jobs/   - View applications
/job/<id>/                 - View job details
/apply/<id>/               - Apply to job
/candidate/view-hr/<id>/   - View HR profile
```

### HR Routes
```
/hr/                       - HR dashboard
/hr/profile/               - HR profile
/hr/post-job/              - Post new job
/hr/edit-job/<id>/         - Edit job posting
/hr/delete-job/<id>/       - Delete job
/hr/candidates/            - View candidates
/hr/view-candidate/<id>/   - View candidate profile
/hr/job-history/           - Job posting history
/hr/aboutus/               - Company about page
```

### Public Routes
```
/                          - Home page
/aboutus/                  - About us page
/contactus/                - Contact form
/blog/<id>/                - Blog details
```

---

## Important Django Terminology & Templates

### Template Tags Used
```django
{% url 'url_name' %}                      # Generate URL from URL name
{% csrf_token %}                          # CSRF protection token
{% if condition %} ... {% endif %}        # Conditional rendering
{% for item in list %} ... {% endfor %}   # Loop through collections
{{ variable }}                             # Display variable value
{% load static %}                         # Load static files
{% static 'path/to/file' %}               # Reference static files
{% extends 'base.html' %}                 # Template inheritance
{% block content %} ... {% endblock %}    # Block definition
{% include 'navbar.html' %}               # Include template
```

### Context Variables (Passed from Views to Templates)
```python
context = {
    'jobs': job_list,              # List of job objects
    'candidates': candidate_list,  # List of candidates
    'applications': apps,          # User applications
    'user': request.user,          # Current logged-in user
    'msg': success_message,        # Success/error messages
    'page_obj': paginator,         # Pagination object
}
```

---

## Common Django Commands Used in This Project

```bash
# Database Management
python manage.py migrate                 # Apply migrations
python manage.py makemigrations          # Create new migrations
python manage.py sqlmigrate app 0001    # View SQL for migration

# Development
python manage.py runserver              # Start development server
python manage.py shell                  # Interactive shell
python manage.py dbshell                # Database shell

# User Management
python manage.py createsuperuser        # Create admin user
python manage.py changepassword username # Change user password

# Data Management
python manage.py dumpdata > backup.json # Export database
python manage.py loaddata backup.json   # Import database

# Testing & Debugging
python manage.py test                   # Run tests
python manage.py check                  # Check project setup

# Static Files
python manage.py collectstatic          # Collect static files
```

---

## Models Detailed Documentation

### 1. User Model (extends Django's AbstractUser)
```python
Fields:
- username: Unique username
- email: Email address
- password: Hashed password
- role: Choice field (CANDIDATE, HR, ADMIN)
- is_active: Account activation status
- is_staff: Staff status
- is_superuser: Admin status
- created_at: Registration timestamp

Key Methods:
- get_role_display(): Display user's role
- is_candidate(): Check if candidate
- is_hr(): Check if HR user
```

### 2. Candidate Model
```python
Fields:
- user: OneToOneField to User
- phone: Contact number
- address: Residential address
- city: City
- state: State
- country: Country
- bio: Personal bio/summary
- profile_picture: Profile image
- resume: PDF file
- created_at: Profile creation date

Relationships:
- education: OneToMany with CandidateEducation
- skills: ManyToMany with CandidateSkill
- languages: ManyToMany with CandidateLanguage
- experience: OneToMany with CandidateExperience
```

### 3. CandidateEducation
```python
Fields:
- candidate: ForeignKey to Candidate
- degree: Degree type (Bachelor, Master, etc.)
- institution: School/University name
- field_of_study: Major/Stream
- start_date: Starting date
- end_date: Completion date
- grade: GPA/Marks
```

### 4. CandidateSkill
```python
Fields:
- skill_name: Name of skill
- candidate: ManyToMany relation
- level: Proficiency (Beginner, Intermediate, Advanced, Expert)
```

### 5. CandidateLanguage
```python
Fields:
- candidate: ManyToMany relation
- language_name: Language name
- proficiency: Proficiency level
```

### 6. CandidateExperience
```python
Fields:
- candidate: ForeignKey to Candidate
- company: Company name
- job_title: Job title
- start_date: Start date
- end_date: End date
- description: Job description
```

### 7. Company Model
```python
Fields:
- user: OneToOneField to HR User
- company_name: Official company name
- website: Company website URL
- industry: Industry type
- company_size: Company size
- about: Company description
- logo: Company logo image
- location: Headquarters location
- created_at: Registration timestamp
```

### 8. Job Model
```python
Fields:
- posted_by: ForeignKey to HR User
- company: ForeignKey to Company
- title: Job title
- description: Job details
- requirements: Required qualifications
- salary: Salary range
- location: Job location
- employment_type: Full-time, Part-time, Contract, etc.
- work_mode: On-site, Remote, Hybrid
- experience_level: Entry, Mid, Senior
- posted_at: Posting date
- deadline: Application deadline
- is_active: Job status

Relationships:
- applications: OneToMany with Application
```

### 9. Application Model
```python
Fields:
- candidate: ForeignKey to Candidate
- job: ForeignKey to Job
- applied_at: Application timestamp
- is_shortlisted: Shortlist status (Stage 1)
- is_selected: Final selection status (Stage 2)
- status: Current status (Pending, Reviewed, etc.)

Relationships:
- status_history: OneToMany with ApplicationStatus
```

### 10. ApplicationStatus
```python
Fields:
- application: ForeignKey to Application
- status: Status choice (Applied, Reviewed, Shortlisted, etc.)
- notes: HR notes
- updated_at: Status update timestamp
```

### 11. ContactMessage
```python
Fields:
- name: Sender name
- email: Sender email
- message: Message content
- created_at: Timestamp
- is_read: Read status (for admin tracking)
```

---

## Admin Customizations

### ContactMessageAdmin
```python
list_display = ('id', 'name', 'email', 'message')
readonly_fields = ('name', 'email', 'message', 'created_at')
list_filter = ('created_at',)
search_fields = ('name', 'email')
```

### CandidateAdmin
```python
list_display = ('user__username', 'city', 'country', 'created_at')
search_fields = ('user__username', 'city', 'country')
list_filter = ('country', 'created_at')
```

### CompanyAdmin
```python
list_display = ('company_name', 'user__username', 'industry', 'created_at')
search_fields = ('company_name', 'industry')
list_filter = ('industry', 'created_at')
readonly_fields = ('created_at',)
```

### JobAdmin
```python
list_display = ('title', 'company', 'employment_type', 'posted_at')
search_fields = ('title', 'company__company_name')
list_filter = ('employment_type', 'work_mode', 'posted_at')
readonly_fields = ('posted_at',)
actions = ['mark_inactive', 'mark_active']
```

### ApplicationAdmin
```python
list_display = ('candidate', 'job', 'applied_at', 'is_shortlisted', 'is_selected')
list_filter = ('is_shortlisted', 'is_selected', 'applied_at')
search_fields = ('candidate__user__username', 'job__title')
readonly_fields = ('applied_at',)
actions = ['shortlist_applications']
```

---

## Security Features

1. **CSRF Protection**: {% csrf_token %} in all forms
2. **Password Hashing**: Django's default PBKDF2 algorithm
3. **User Authentication**: Login required decorators (@login_required)
4. **SQL Injection Prevention**: Django ORM parameterized queries
5. **SQL Injection Prevention in Raw Queries**: Always use .filter() instead of raw SQL
6. **Access Control**: Role-based access (is_candidate, is_hr)
7. **Admin Restriction**: Admin operations only for superusers
8. **Email Validation**: Built-in Django email validation
9. **HTTPS Ready**: CSRF cookie settings configured
10. **XSS Protection**: Django template auto-escaping enabled

---

## Authentication Flow

```
User Registration
    ↓
Select Role (Candidate/HR) 
    ↓
Create Account (Unique Email/Username)
    ↓
Password Hashing & Storage
    ↓
Email Verification (Optional)
    ↓
Login with Credentials
    ↓
Session Management
    ↓
Role-based Dashboard Access
```

---

## Recruitment Workflow

```
HR posts job
    ↓
Job appears in candidate search
    ↓
Candidate views job details
    ↓
Candidate applies to job
    ↓
HR receives application notification
    ↓
HR reviews candidate profile
    ↓
HR shortlists candidate (Stage 1)
    ↓
HR makes final selection (Stage 2)
    ↓
Application status updated to "Selected"
    ↓
Candidate notified
```

---

## Advanced Features

### Job Search Filters
- **Keyword Search**: Search by job title, description, company name
- **Location Filter**: Search jobs by location
- **Salary Range**: Filter jobs by minimum-maximum salary
- **Employment Type**: Full-time, Part-time, Contract, Temporary
- **Work Mode**: On-site, Remote, Hybrid
- **Experience Level**: Entry, Mid, Senior
- **Date Range**: Filter jobs posted in last X days

### Pagination
- Default 10 items per page
- Available for jobs list, candidates list, applications list
- URL parameter: `?page=2`

### Two-Stage Shortlisting
- **Stage 1 (Shortlist)**: HR marks promising candidates
- **Stage 2 (Final Selection)**: HR makes final hiring decision
- Each stage maintains status history with notes

### Profile Management
- Candidates can add education, experience, skills, languages
- HR can manage company information
- Candidates can upload resume and profile picture

---

## Deployment Checklist

```
Before Production:
- [ ] Update SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure allowed HOSTS
- [ ] Set up email backend for notifications
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure static files for production
- [ ] Set up media file storage
- [ ] Configure HTTPS and CSRF settings
- [ ] Run security checks: python manage.py check --deploy
- [ ] Set up database backups
- [ ] Configure proper logging
```

---

## Troubleshooting Common Issues

### Issue: Migration Failed
```bash
Solution: python manage.py migrate --fake-initial
```

### Issue: Static Files Not Loading
```bash
Solution: python manage.py collectstatic --noinput
```

### Issue: Login Not Working
```bash
Solution: Check INSTALLED_APPS includes 'django.contrib.auth'
         Check SESSION_ENGINE setting
```

### Issue: Email Not Sending
```bash
Solution: Configure EMAIL_BACKEND in settings.py
         Add EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```

---

## Contributing Guidelines

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test your changes: `python manage.py test`
4. Commit your changes: `git commit -m 'Add new feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Create a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Contact & Support

For questions or support, contact:
- Email: support@jobportal.com
- GitHub: https://github.com/Dipesh-Dhaurali/JobPortal

---

## Project Statistics

- **Total Models**: 11
- **Total Views**: 30+
- **Total URLs**: 25+
- **Total Templates**: 24
- **Code Lines**: 3000+
- **Database Tables**: 12
- **Admin Customizations**: 8

---

## Future Enhancements

1. Email notifications on application status
2. Interview scheduling feature
3. Resume parsing with AI
4. Video interview integration
5. Skill assessment tests
6. Social media profile linking
7. Advanced analytics dashboard
8. Payment integration for premium features
9. Mobile app (React Native/Flutter)
10. Real-time notifications (WebSocket)
