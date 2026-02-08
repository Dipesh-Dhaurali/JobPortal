# Job Portal - API & URL Documentation

## Complete URL Routing Guide

### Authentication URLs
Base Path: `/`

| URL | Method | View | Purpose | Access |
|-----|--------|------|---------|--------|
| `/login/` | GET, POST | `loginuser` | User login | Public |
| `/register/` | GET | Registration options | Show role selection | Public |
| `/candidate-register/` | GET, POST | `candidateregister` | Candidate registration | Public |
| `/hr-register/` | GET, POST | `hrregister` | HR registration | Public |
| `/logout/` | GET | `logoutuser` | Logout user | Authenticated |
| `/` | GET | `home` / `index` | Homepage | Public |

---

## Candidate URLs
Base Path: `/candidate/`

| URL | Method | View | Purpose | Access |
|-----|--------|------|---------|--------|
| `/candidate/` | GET | `candidatedashboard` | Candidate dashboard | Candidate |
| `/candidate/dashboard/` | GET | `dashboard` | Candidate dashboard alternative | Candidate |
| `/candidate/profile/` | GET, POST | `candidateprofile` | View/edit profile | Candidate |
| `/candidate/applied-jobs/` | GET | `appliedjobs` | View submitted applications | Candidate |
| `/candidate/view-hr/<id>/` | GET | `viewhrprofile` | View HR company profile | Candidate |
| `/job/<id>/` | GET | `jobdetail` | View job details | Candidate |
| `/apply/<id>/` | POST | `applyjob` | Apply to job | Candidate |

---

## HR/Recruiter URLs
Base Path: `/hr/`

| URL | Method | View | Purpose | Access |
|-----|--------|------|---------|--------|
| `/hr/` | GET | `hrdashboard` | HR main dashboard | HR |
| `/hr/profile/` | GET, POST | `hrprofile` | View/edit HR profile | HR |
| `/hr/post-job/` | GET, POST | `postjob` | Create new job posting | HR |
| `/hr/edit-job/<id>/` | GET, POST | `editjob` | Edit existing job | HR |
| `/hr/delete-job/<id>/` | GET, POST | `deletejob` | Delete job posting | HR |
| `/hr/candidates/` | GET | `candidates` | View candidate list | HR |
| `/hr/view-candidate/<id>/` | GET | `viewcandidateprofile` | View candidate profile | HR |
| `/hr/job-history/` | GET | `jobhistory` | View all posted jobs | HR |
| `/hr/aboutus/` | GET | `aboutus` | Company about page | HR |
| `/hr/blog/<id>/` | GET | `blogdetail` | Blog/article details | HR |

---

## Public URLs
Base Path: `/`

| URL | Method | View | Purpose | Access |
|-----|--------|------|---------|--------|
| `/` | GET | `home` / `index` | Homepage | Public |
| `/aboutus/` | GET | `aboutus` | About us page | Public |
| `/contactus/` | GET, POST | `contactus` | Contact form | Public |
| `/blog/<id>/` | GET | `blog_detail` | Blog post details | Public |

---

## Admin URLs
Base Path: `/admin/`

| URL | Method | Purpose | Access |
|-----|--------|---------|--------|
| `/admin/` | GET, POST | Django admin dashboard | Admin/Superuser |
| `/admin/authuser/user/` | GET, POST | Manage users | Admin |
| `/admin/candidate/candidate/` | GET, POST | Manage candidates | Admin |
| `/admin/candidate/candidateeducation/` | GET, POST | Manage education records | Admin |
| `/admin/hr/company/` | GET, POST | Manage companies | Admin |
| `/admin/hr/job/` | GET, POST | Manage jobs | Admin |
| `/admin/hr/application/` | GET, POST | Manage applications | Admin |
| `/admin/authuser/contactmessage/` | GET, POST | Manage messages | Admin |

---

## Form Data & Request Methods

### Login Form (POST to `/login/`)
```
Fields:
- username: Text (required)
- password: Password (required)

Response:
- Success: Redirect to dashboard based on role
- Failure: Show error message, reload login page
```

### Candidate Registration (POST to `/candidate-register/`)
```
Fields:
- username: Text (unique, required)
- email: Email (unique, required)
- password: Password (required)
- password_confirm: Password (must match, required)
- first_name: Text (required)
- last_name: Text (required)
- phone: Phone number (required)
- address: Text
- city: Text
- state: Text
- country: Text

Response:
- Success: Account created, redirect to login
- Failure: Show validation errors
```

### HR Registration (POST to `/hr-register/`)
```
Fields:
- username: Text (unique, required)
- email: Email (unique, required)
- password: Password (required)
- password_confirm: Password (required)
- company_name: Text (required)
- company_website: URL
- industry: Select dropdown
- company_size: Select dropdown
- company_location: Text
- first_name: Text
- last_name: Text

Response:
- Success: Account created, company profile created
- Failure: Show validation errors
```

### Post Job Form (POST to `/hr/post-job/`)
```
Fields:
- title: Text (required)
- description: Textarea (required)
- requirements: Textarea (required)
- salary: Text/Number (required)
- location: Text (required)
- employment_type: Select (required)
- work_mode: Select (required)
- experience_level: Select (required)
- deadline: Date (required)

Response:
- Success: Job created, show success message
- Failure: Show form errors

Employment Type Choices:
- Full-time
- Part-time
- Contract
- Temporary

Work Mode Choices:
- On-site
- Remote
- Hybrid

Experience Level Choices:
- Entry
- Mid
- Senior
```

### Apply Job Form (POST to `/apply/<job_id>/`)
```
Fields:
- (No additional form, application created directly)

Response:
- Success: Application created, show "Applied successfully"
- Failure: "Already applied" or "Job closed"
```

### Candidate Profile Form (POST to `/candidate/profile/`)
```
Editable Fields:
- phone: Text
- address: Text
- city: Text
- state: Text
- country: Text
- bio: Textarea
- profile_picture: File upload
- resume: File upload

Education Section:
- degree: Select (Bachelor, Master, Diploma, etc.)
- institution: Text
- field_of_study: Text
- start_date: Date
- end_date: Date
- grade: Text

Experience Section:
- company: Text
- job_title: Text
- start_date: Date
- end_date: Date
- description: Textarea

Skills Section:
- Add skills with proficiency level (Beginner, Intermediate, Advanced, Expert)

Languages Section:
- Add languages with proficiency level
```

### HR Profile Form (POST to `/hr/profile/`)
```
Editable Fields:
- company_name: Text
- company_website: URL
- industry: Select
- company_size: Select
- about: Textarea
- logo: File upload
- location: Text
```

### Contact Form (POST to `/contactus/`)
```
Fields:
- name: Text (required)
- email: Email (required)
- message: Textarea (required)

Response:
- Success: Message saved, show "Thank you for your message"
- Failure: Show validation errors

Database Action:
- ContactMessage record created with is_read=False
- Admin can view in Django admin
```

---

## Query Parameters & Filters

### Job Search Filters (Query String)
URL: `/candidate/?[filters]`

| Parameter | Values | Example |
|-----------|--------|---------|
| `keyword` | String | `?keyword=python` |
| `location` | String | `?location=New York` |
| `min_salary` | Number | `?min_salary=50000` |
| `max_salary` | Number | `?max_salary=100000` |
| `employment_type` | Choices | `?employment_type=Full-time` |
| `work_mode` | Choices | `?work_mode=Remote` |
| `experience_level` | Choices | `?experience_level=Mid` |
| `posted_after_days` | Number | `?posted_after_days=7` |
| `page` | Number | `?page=2` |

Combined Example:
```
/candidate/?keyword=developer&location=Mumbai&employment_type=Full-time&min_salary=50000&page=1
```

---

## Response Examples

### Successful Login Response
```
HTTP 302 Redirect
Location: /candidate/  (for candidates)
Location: /hr/        (for HR users)
Session: user_id saved in session
```

### Job List Response (Template Context)
```python
{
    'jobs': [
        {
            'id': 1,
            'title': 'Senior Developer',
            'company': 'Tech Corp',
            'location': 'Mumbai',
            'salary': '50000-100000',
            'employment_type': 'Full-time',
            'work_mode': 'Remote',
            'posted_at': '2024-02-08',
            'deadline': '2024-02-28'
        },
        # ... more jobs
    ],
    'page_obj': <Page 1 of 5>,
    'total_count': 50
}
```

### Candidate Detail Response
```python
{
    'candidate': {
        'user': {'username': 'john_doe', 'email': 'john@email.com'},
        'phone': '+91-9876543210',
        'city': 'Mumbai',
        'state': 'Maharashtra',
        'country': 'India',
        'bio': 'Experienced developer',
        'education': [
            {
                'degree': 'Bachelor',
                'institution': 'XYZ University',
                'field_of_study': 'Computer Science',
                'end_date': '2022-06-15'
            }
        ],
        'experience': [
            {
                'company': 'ABC Company',
                'job_title': 'Developer',
                'start_date': '2022-07-01'
            }
        ],
        'skills': ['Python', 'Django', 'JavaScript'],
        'languages': ['English', 'Hindi']
    }
}
```

### Application Status Response
```python
{
    'application': {
        'id': 5,
        'candidate': 'john_doe',
        'job': 'Senior Developer',
        'applied_at': '2024-02-05 10:30:00',
        'is_shortlisted': True,
        'is_selected': False,
        'status_history': [
            {
                'status': 'Applied',
                'updated_at': '2024-02-05',
                'notes': 'Initial application'
            },
            {
                'status': 'Reviewed',
                'updated_at': '2024-02-06',
                'notes': 'Profile reviewed'
            },
            {
                'status': 'Shortlisted',
                'updated_at': '2024-02-07',
                'notes': 'Shortlisted for interview'
            }
        ]
    }
}
```

---

## Error Responses

### 404 - Job Not Found
```
User tries to apply to non-existent job
Response: 404 Page or redirect to home
```

### 403 - Permission Denied
```
Candidate tries to access HR dashboard
Response: Redirect to candidate dashboard or show 403 error
```

### 400 - Invalid Form Data
```
Submitted form with missing required fields
Response: Reload form with error messages highlighted
```

### 500 - Server Error
```
Unexpected error in view
Response: Show generic error page or error message
```

---

## Pagination

### Default Pagination
- Items per page: 10
- Query parameter: `page=<number>`

### Pagination Template Usage
```django
{% if page_obj.has_previous %}
    <a href="?page=1">First</a>
    <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
{% endif %}

Current page: {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}

{% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}">Next</a>
    <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
{% endif %}
```

---

## User Authentication & Sessions

### Session Management
```python
# Create session on login
login(request, user)

# Check if user is authenticated
if request.user.is_authenticated:
    # User is logged in
    
# Get current user
current_user = request.user

# Get user role
if current_user.role == 'CANDIDATE':
    # Candidate specific logic
```

### Required Decorators for Views
```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def protected_view(request):
    # Only authenticated users can access
```

---

## AJAX & Dynamic Calls

### Shortlist Candidate (if implemented)
```
POST /api/shortlist/<application_id>/
Headers: Content-Type: application/json
Body: { "is_shortlisted": true }
Response: { "success": true, "message": "Candidate shortlisted" }
```

### Update Application Status (if implemented)
```
POST /api/update-status/<application_id>/
Headers: Content-Type: application/json
Body: { "status": "Reviewed", "notes": "Good fit" }
Response: { "success": true, "status": "Reviewed" }
```

---

## Rate Limiting & Throttling
(Not currently implemented, recommendations for future):
- Limit job applications per candidate per day: 5 applications/day
- Limit job postings per HR per day: 10 jobs/day
- Limit login attempts: 5 attempts per 5 minutes

---

## Common HTTP Status Codes Used
```
200 OK           - Successful GET request
201 Created      - Successful POST request (resource created)
302 Found        - Redirect (successful login)
304 Not Modified - Cache-related response
400 Bad Request  - Invalid form data
403 Forbidden    - User doesn't have permission
404 Not Found    - Resource/page not found
500 Server Error - Backend error
```

---

## Testing API Endpoints

### Using cURL Examples

**Test login:**
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=password123"
```

**Test candidate registration:**
```bash
curl -X POST http://localhost:8000/candidate-register/ \
  -d "username=jane_doe&email=jane@email.com&password=pass123&phone=9876543210"
```

**Test job posting:**
```bash
curl -X POST http://localhost:8000/hr/post-job/ \
  -d "title=Developer&salary=50000&location=Mumbai&employment_type=Full-time"
```

---

## Webhooks & Notifications (Future Enhancement)
```
Candidate applies for job:
- Webhook to: HR's notification system
- Data: {application_id, candidate_name, job_title}

HR shortlists candidate:
- Webhook to: Candidate's email
- Data: {candidate_name, job_title, shortlist_date}
```
