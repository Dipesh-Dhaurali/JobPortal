# Job Portal - Setup & Deployment Guide

## Complete Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git
- Virtual environment support
- A code editor (VS Code, PyCharm, etc.)

### Step-by-Step Installation

#### 1. Clone Repository
```bash
git clone https://github.com/Dipesh-Dhaurali/JobPortal.git
cd JobPortal
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install django==5.2.3
pip install pillow          # For image handling
pip install python-decouple # For environment variables (optional)
```

Or use requirements.txt if available:
```bash
pip install -r requirements.txt
```

#### 4. Database Setup
```bash
# Create database tables
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Enter username: admin
# Enter email: admin@example.com
# Enter password: (choose secure password)

# (Optional) Load sample data
python manage.py loaddata sample_data.json
```

#### 5. Create Media Folders
```bash
mkdir -p media/profiles
mkdir -p media/resumes
mkdir -p media/logos
```

#### 6. Run Development Server
```bash
python manage.py runserver
```

Access the application:
- Main Portal: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Default admin credentials: username/password set in step 4

---

## Environment Configuration

### settings.py Key Settings

#### DEBUG Mode
```python
# Development
DEBUG = True

# Production
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

#### Database Configuration
```python
# SQLite (Default - Development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (Production - Recommended)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'jobportal_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### Static Files Configuration
```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# For production
STATIC_ROOT = '/var/www/jobportal/staticfiles/'
```

#### Media Files Configuration
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# urls.py - Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### Email Configuration (for notifications)
```python
# Gmail (Gmail App Password required)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

# SendGrid
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your_api_key'
```

#### Installed Apps
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authuser',    # Custom auth app
    'candidate',   # Candidate app
    'hr',          # HR/recruiter app
]
```

#### Middleware
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

---

## Testing the Application

### Basic Functionality Tests

#### 1. Registration Test
1. Navigate to `/candidate-register/`
2. Fill registration form
3. Submit and verify account creation
4. Login with new credentials
5. Verify redirect to candidate dashboard

#### 2. Job Posting Test
1. Register as HR
2. Navigate to `/hr/post-job/`
3. Fill job details
4. Submit and verify job creation
5. Check job appears in candidate search

#### 3. Application Test
1. Login as candidate
2. Search and view jobs
3. Click Apply on a job
4. Verify application appears in `/candidate/applied-jobs/`
5. Verify appears in HR dashboard

#### 4. Admin Test
1. Go to `/admin/`
2. Login as superuser
3. Verify all models accessible
4. Test filtering and searching
5. Test bulk actions

### Running Django Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test authuser
python manage.py test candidate
python manage.py test hr

# Run with verbose output
python manage.py test --verbosity=2

# Run specific test class
python manage.py test authuser.tests.UserRegistrationTest
```

---

## Deployment to Production

### Pre-Deployment Checklist

```bash
# 1. Security checks
python manage.py check --deploy

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Check for missing migrations
python manage.py makemigrations --check

# 4. Run tests
python manage.py test

# 5. Check code style (optional)
flake8 .
```

### Production Settings Changes

#### settings.py for Production
```python
# Security
DEBUG = False
SECRET_KEY = 'your-secret-key-from-environment'  # Use env variables
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - Use PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# CSRF and Security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# SSL/HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### Using Environment Variables
```python
# .env file (don't commit to git)
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/jobportal
EMAIL_HOST_PASSWORD=your-email-password

# settings.py
import os
from pathlib import Path
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')
```

### Deployment to Heroku

#### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download installer from https://devcenter.heroku.com/articles/heroku-cli

# Verify installation
heroku --version
```

#### 2. Create requirements.txt
```bash
pip freeze > requirements.txt
```

Add to requirements.txt:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9
python-decouple==3.8
whitenoise==6.6.0
```

#### 3. Create Procfile
```
# Procfile
web: gunicorn jobportal.wsgi --log-file -
release: python manage.py migrate
worker: python manage.py process_tasks
```

#### 4. Create runtime.txt (optional)
```
python-3.11.5
```

#### 5. Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create jobportal-app

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS='jobportal-app.herokuapp.com'

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

### Deployment to AWS EC2

#### 1. Launch EC2 Instance
```bash
# Ubuntu 20.04 LTS recommended
# Security group: Allow 80, 443, 22

# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 2. Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql nginx git

# Create app directory
mkdir /var/www/jobportal
cd /var/www/jobportal

# Clone repository
git clone https://github.com/Dipesh-Dhaurali/JobPortal.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

#### 3. Configure PostgreSQL
```bash
sudo -u postgres psql

-- Create database and user
CREATE DATABASE jobportal_db;
CREATE USER jobportal_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE jobportal_db TO jobportal_user;
\q
```

#### 4. Configure Django
```bash
# Create .env file
nano /var/www/jobportal/.env

# Add:
SECRET_KEY='your-secret-key'
DEBUG=False
DATABASE_URL=postgresql://jobportal_user:your_password@localhost:5432/jobportal_db
ALLOWED_HOSTS=your-domain.com

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

#### 5. Configure Gunicorn
```bash
# Test Gunicorn
gunicorn --bind 0.0.0.0:8000 jobportal.wsgi

# Create systemd service
sudo nano /etc/systemd/system/jobportal.service

[Unit]
Description=Job Portal Django App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/jobportal
ExecStart=/var/www/jobportal/venv/bin/gunicorn --bind 127.0.0.1:8000 jobportal.wsgi
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable jobportal
sudo systemctl start jobportal
```

#### 6. Configure Nginx
```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/jobportal

upstream jobportal {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 100M;

    location /static/ {
        alias /var/www/jobportal/staticfiles/;
    }

    location /media/ {
        alias /var/www/jobportal/media/;
    }

    location / {
        proxy_pass http://jobportal;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/jobportal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL Certificate (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl restart nginx
```

---

## Maintenance & Monitoring

### Regular Maintenance Tasks

```bash
# Weekly: Backup database
python manage.py dumpdata > backup-$(date +%Y%m%d).json

# Monthly: Check for security updates
pip list --outdated
pip install --upgrade django

# Monitor disk space
df -h

# Monitor logs
tail -f /var/log/django/error.log

# Clear old sessions
python manage.py clearsessions

# Verify database integrity
python manage.py dbshell
PRAGMA integrity_check;
```

### Common Troubleshooting

#### Static Files Not Loading
```bash
# Collect static files again
python manage.py collectstatic --noinput --clear

# Check permissions
sudo chown -R www-data:www-data /var/www/jobportal/staticfiles
```

#### Database Locked
```bash
# Check processes
lsof /path/to/db.sqlite3

# Restart database service
sudo systemctl restart postgresql
```

#### Gunicorn Not Responding
```bash
# Check service status
sudo systemctl status jobportal

# View logs
journalctl -u jobportal -n 50

# Restart service
sudo systemctl restart jobportal
```

#### Email Not Sending
```python
# Test email in Django shell
python manage.py shell

from django.core.mail import send_mail
send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

---

## Performance Optimization

### Database Optimization
```python
# Enable query caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Use select_related and prefetch_related
jobs = Job.objects.select_related('company').all()
candidates = Candidate.objects.prefetch_related('skills').all()
```

### Caching Headers
```python
from django.views.decorators.http import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def job_list(request):
    return render(request, 'jobs.html')
```

### Compression
```python
# Enable GZIP compression in Nginx
gzip on;
gzip_types text/plain text/css text/javascript application/json;
gzip_min_length 1000;
```

---

## Backup & Recovery

### Automated Backups
```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/jobportal"
DATE=$(date +%Y%m%d)

# Database backup
pg_dump jobportal_db > $BACKUP_DIR/db_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/jobportal/media/

# Keep only 30 days of backups
find $BACKUP_DIR -mtime +30 -delete
```

### Recovery Process
```bash
# Restore database
psql jobportal_db < backup-20240208.sql

# Restore media
tar -xzf media_20240208.tar.gz -C /var/www/jobportal/
```

---

## Version Control & Collaboration

### Git Workflow
```bash
# Clone repository
git clone https://github.com/Dipesh-Dhaurali/JobPortal.git

# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request on GitHub
# After review and approval, merge to main
```

### Ignoring Files (.gitignore)
```
*.pyc
__pycache__/
*.py[cod]
*$py.class
.env
db.sqlite3
venv/
staticfiles/
/media
.vscode/
.DS_Store
```

---

## Production Monitoring

### Key Metrics to Monitor
- Application response time
- Database query time
- Error rate
- User count
- Storage space
- CPU/Memory usage

### Tools for Monitoring
- **Sentry**: Error tracking and monitoring
- **New Relic**: Application performance monitoring
- **DataDog**: Infrastructure monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Data visualization

### Basic Health Check Endpoint (optional)
```python
# urls.py
def health_check(request):
    return JsonResponse({'status': 'healthy'})

urlpatterns = [
    path('health/', health_check),
]
```
