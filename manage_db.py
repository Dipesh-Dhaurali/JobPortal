#!/usr/bin/env python
"""
Database Management Script for JobPortal
This script handles all database initialization and seeding
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from django.contrib.auth.models import User
from authuser.models import UserProfile
from hr.models import hr, JobPost, candidateApplication, HRProfile
from candidate.models import CandidateProfile, MyApplyJobList, IsShortlisted
from admin_portal.models import AdminUser, UserStatus, AdminActivityLog

def delete_all_data():
    """Delete all existing data from database"""
    print("Deleting existing data...")
    User.objects.all().delete()
    print("✓ All data cleared")

def create_admin_user():
    """Create admin user"""
    print("\n--- Creating Admin User ---")
    
    admin_user = User.objects.create_user(
        username='admin_user',
        email='admin@jobportal.com',
        password='admin123',
        first_name='Admin',
        last_name='Portal'
    )
    
    # Create UserProfile for admin
    UserProfile.objects.create(
        user=admin_user,
        user_type='admin',
        phone_number='+977-1-4200000',
        is_verified=True
    )
    
    # Create AdminUser instance
    admin_portal = AdminUser.objects.create(
        user=admin_user,
        is_super_admin=True
    )
    
    # Create UserStatus for admin
    UserStatus.objects.create(
        user=admin_user,
        user_type='hr',
        status='active'
    )
    
    print(f"✓ Admin user created: {admin_user.username}")
    print(f"  - Email: {admin_user.email}")
    print(f"  - Password: admin123")
    return admin_user

def create_hr_users():
    """Create HR/Company users"""
    print("\n--- Creating HR Users ---")
    
    hr_data = [
        {
            'username': 'tech_company_hr',
            'email': 'hr@techcorp.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'company_name': 'TechCorp Solutions',
            'industry': 'technology',
            'company_type': 'startup',
            'employee_size': '51-200',
            'location': 'Kathmandu, Nepal',
            'about': 'Leading technology solutions provider specializing in web and mobile development.',
            'website': 'https://techcorp.com',
            'linkedin': 'https://linkedin.com/company/techcorp',
            'phone': '+977-1-4200001'
        },
        {
            'username': 'finance_company_hr',
            'email': 'careers@financepro.com',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'company_name': 'FinancePro Services',
            'industry': 'finance',
            'company_type': 'private',
            'employee_size': '201-500',
            'location': 'Pokhara, Nepal',
            'about': 'Digital financial services platform providing banking and investment solutions.',
            'website': 'https://financepro.com',
            'linkedin': 'https://linkedin.com/company/financepro',
            'phone': '+977-1-4200002'
        },
        {
            'username': 'health_company_hr',
            'email': 'jobs@healthsystem.com',
            'first_name': 'Dr. Michael',
            'last_name': 'Wilson',
            'company_name': 'HealthSystem Ltd',
            'industry': 'healthcare',
            'company_type': 'private',
            'employee_size': '501-1000',
            'location': 'Biratnagar, Nepal',
            'about': 'Comprehensive healthcare provider with modern medical facilities and research center.',
            'website': 'https://healthsystem.com',
            'linkedin': 'https://linkedin.com/company/healthsystem',
            'phone': '+977-1-4200003'
        },
    ]
    
    created_hrs = []
    for data in hr_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='hr@123456',
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='hr',
            phone_number=data['phone'],
            is_verified=True
        )
        
        # Create hr model instance
        hr_obj = hr.objects.create(user=user)
        
        # Create HRProfile
        profile = HRProfile.objects.create(
            user=user,
            company_name=data['company_name'],
            industry=data['industry'],
            company_type=data['company_type'],
            employee_size=data['employee_size'],
            email=data['email'],
            phone_number=data['phone'],
            website=data['website'],
            location=data['location'],
            about_company=data['about'],
            linkedin_url=data['linkedin']
        )
        
        # Create UserStatus
        UserStatus.objects.create(
            user=user,
            user_type='hr',
            status='active'
        )
        
        created_hrs.append(user)
        print(f"✓ HR created: {user.username} - {data['company_name']}")
    
    return created_hrs

def create_candidate_users():
    """Create Candidate users"""
    print("\n--- Creating Candidate Users ---")
    
    candidate_data = [
        {
            'username': 'john_candidate',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+977-9840000001',
            'job_preference': 'Software Engineer',
            'job_level': 'mid',
            'job_type': 'fulltime',
            'experience': 3,
            'education': 'bachelor',
            'program': 'Computer Science',
            'gpa_type': 'gpa_4',
            'gpa_value': 3.8,
            'school': 'Tribhuvan University',
            'graduation': '2021',
            'skills': 'Python, Django, JavaScript, React, Docker, PostgreSQL',
            'languages': 'English, Nepali, Hindi'
        },
        {
            'username': 'sarah_designer',
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Williams',
            'phone': '+977-9840000002',
            'job_preference': 'UI/UX Designer',
            'job_level': 'senior',
            'job_type': 'fulltime',
            'experience': 5,
            'education': 'bachelor',
            'program': 'Graphic Design',
            'gpa_type': 'percentage',
            'gpa_value': 92.5,
            'school': 'Kathmandu University of Arts',
            'graduation': '2019',
            'skills': 'Figma, Adobe XD, Photoshop, Illustrator, UI Design, Wireframing',
            'languages': 'English, Nepali'
        },
        {
            'username': 'alex_marketer',
            'email': 'alex@example.com',
            'first_name': 'Alex',
            'last_name': 'Brown',
            'phone': '+977-9840000003',
            'job_preference': 'Digital Marketing Manager',
            'job_level': 'mid',
            'job_type': 'fulltime',
            'experience': 2,
            'education': 'masters',
            'program': 'Marketing Management',
            'gpa_type': 'gpa_10',
            'gpa_value': 8.5,
            'school': 'Nepal Academy of Business',
            'graduation': '2022',
            'skills': 'SEO, Social Media Marketing, Google Analytics, Content Writing, Email Marketing',
            'languages': 'English, Nepali, Spanish'
        },
        {
            'username': 'emma_developer',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Davis',
            'phone': '+977-9840000004',
            'job_preference': 'Full Stack Developer',
            'job_level': 'junior',
            'job_type': 'fulltime',
            'experience': 1,
            'education': 'bachelor',
            'program': 'Information Technology',
            'gpa_type': 'percentage',
            'gpa_value': 88.0,
            'school': 'Nepal Institute of Technology',
            'graduation': 'currently_running',
            'skills': 'JavaScript, Node.js, MongoDB, HTML, CSS, Express.js',
            'languages': 'English, Nepali'
        },
        {
            'username': 'michael_analyst',
            'email': 'michael@example.com',
            'first_name': 'Michael',
            'last_name': 'Garcia',
            'phone': '+977-9840000005',
            'job_preference': 'Data Analyst',
            'job_level': 'mid',
            'job_type': 'fulltime',
            'experience': 4,
            'education': 'bachelor',
            'program': 'Statistics',
            'gpa_type': 'gpa_4',
            'gpa_value': 3.6,
            'school': 'Kathmandu University',
            'graduation': '2020',
            'skills': 'Python, SQL, Tableau, Excel, Power BI, Statistics',
            'languages': 'English, Nepali, Mandarin'
        },
    ]
    
    created_candidates = []
    for data in candidate_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='candidate@123456',
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        
        # Create UserProfile
        UserProfile.objects.create(
            user=user,
            user_type='candidate',
            phone_number=data['phone'],
            is_verified=True
        )
        
        # Create CandidateProfile
        profile = CandidateProfile.objects.create(
            user=user,
            job_preference_title=data['job_preference'],
            preferred_job_level=data['job_level'],
            preferred_job_type=data['job_type'],
            work_experience=data['experience'],
            education_level=data['education'],
            course_or_program=data['program'],
            gpa_percentage_type=data['gpa_type'],
            gpa_percentage_value=data['gpa_value'],
            school_college_name=data['school'],
            graduation_year=data['graduation'],
            skills=data['skills'],
            languages=data['languages']
        )
        
        # Create UserStatus
        UserStatus.objects.create(
            user=user,
            user_type='candidate',
            status='active'
        )
        
        created_candidates.append(user)
        print(f"✓ Candidate created: {user.username} - {data['job_preference']}")
    
    return created_candidates

def create_job_posts(hr_users):
    """Create job postings"""
    print("\n--- Creating Job Posts ---")
    
    jobs = [
        {
            'hr_user': hr_users[0],
            'title': 'Senior Python Developer',
            'company_name': 'TechCorp Solutions',
            'address': 'Kathmandu, Nepal',
            'salary_low': 80000,
            'salary_high': 120000,
            'employment_type': 'full-time',
            'work_mode': 'hybrid',
            'days_open': 30
        },
        {
            'hr_user': hr_users[0],
            'title': 'React.js Frontend Developer',
            'company_name': 'TechCorp Solutions',
            'address': 'Kathmandu, Nepal',
            'salary_low': 60000,
            'salary_high': 90000,
            'employment_type': 'full-time',
            'work_mode': 'remote',
            'days_open': 15
        },
        {
            'hr_user': hr_users[1],
            'title': 'Financial Analyst',
            'company_name': 'FinancePro Services',
            'address': 'Pokhara, Nepal',
            'salary_low': 55000,
            'salary_high': 80000,
            'employment_type': 'full-time',
            'work_mode': 'on-site',
            'days_open': 20
        },
        {
            'hr_user': hr_users[2],
            'title': 'Healthcare Administrator',
            'company_name': 'HealthSystem Ltd',
            'address': 'Biratnagar, Nepal',
            'salary_low': 40000,
            'salary_high': 60000,
            'employment_type': 'full-time',
            'work_mode': 'on-site',
            'days_open': 25
        },
    ]
    
    created_jobs = []
    for job_data in jobs:
        last_date = datetime.now().date() + timedelta(days=job_data['days_open'])
        
        job = JobPost.objects.create(
            user=job_data['hr_user'],
            title=job_data['title'],
            address=job_data['address'],
            CompanyName=job_data['company_name'],
            salaryLow=job_data['salary_low'],
            salaryHigh=job_data['salary_high'],
            employment_type=job_data['employment_type'],
            work_mode=job_data['work_mode'],
            lastDateToApply=last_date,
            applycount=0
        )
        
        created_jobs.append(job)
        print(f"✓ Job created: {job.title} at {job.CompanyName}")
    
    return created_jobs

def create_applications(candidates, jobs):
    """Create job applications"""
    print("\n--- Creating Job Applications ---")
    
    applications_map = [
        (0, 0), (0, 1), (1, 2),  # john applies to tech jobs
        (1, 0), (1, 2),           # sarah applies to various
        (2, 3), (2, 2),           # alex applies
        (3, 0), (3, 1),           # emma applies to dev jobs
        (4, 2), (4, 3),           # michael applies
    ]
    
    created_apps = []
    for candidate_idx, job_idx in applications_map:
        try:
            app = candidateApplication.objects.create(
                user=candidates[candidate_idx],
                job=jobs[job_idx],
                education_level='bachelor',
                passingYear='2021',
                yearOfExp=candidate_idx + 1,
                status='pending'
            )
            created_apps.append(app)
            print(f"✓ Application: {candidates[candidate_idx].username} -> {jobs[job_idx].title}")
        except Exception as e:
            print(f"  ! Skipped duplicate application: {str(e)}")
    
    return created_apps

def create_shortlists(applications):
    """Create some shortlisted candidates"""
    print("\n--- Creating Shortlists ---")
    
    # Shortlist first 3 applications
    for app in applications[:3]:
        try:
            IsShortlisted.objects.create(
                user=app.user,
                job=app.job
            )
            print(f"✓ Shortlisted: {app.user.username} for {app.job.title}")
        except Exception as e:
            print(f"  ! Skip: {str(e)}")

def main():
    """Main execution function"""
    print("=" * 60)
    print("JobPortal Database Initialization Script")
    print("=" * 60)
    
    try:
        # Clear existing data
        delete_all_data()
        
        # Create users
        admin = create_admin_user()
        hr_users = create_hr_users()
        candidates = create_candidate_users()
        
        # Create jobs and applications
        jobs = create_job_posts(hr_users)
        applications = create_applications(candidates, jobs)
        
        # Create shortlists
        create_shortlists(applications)
        
        print("\n" + "=" * 60)
        print("✓ Database initialization completed successfully!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print("  Admin - Username: admin_user | Password: admin123")
        print("  HR - Username: tech_company_hr | Password: hr@123456")
        print("  Candidate - Username: john_candidate | Password: candidate@123456")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
