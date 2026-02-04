import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobportal.settings')
django.setup()

from django.contrib.auth.models import User
from hr.models import hr, JobPost, HRProfile, candidateApplication
from candidate.models import CandidateProfile
from admin_portal.models import AdminUser, UserStatus

def clear_existing_data():
    """Clear existing test data"""
    print("Clearing existing data...")
    User.objects.filter(username__startswith='test_').delete()
    User.objects.filter(username='admin_user').delete()
    print("✓ Cleared existing test data")

def create_admin():
    """Create admin user"""
    print("\nCreating admin user...")
    admin_user = User.objects.create_user(
        username='admin_user',
        email='admin@jobportal.com',
        password='admin123',
        first_name='Admin',
        last_name='Portal',
        is_staff=True
    )
    
    # Create AdminUser relationship
    AdminUser.objects.create(user=admin_user)
    
    # Create status record
    UserStatus.objects.create(user=admin_user, status='active')
    
    print(f"✓ Admin user created: admin_user / admin123")
    print(f"  Email: admin@jobportal.com")
    return admin_user

def create_hr_users():
    """Create HR/Company users"""
    print("\nCreating HR users...")
    hr_list = []
    
    companies = [
        {
            'username': 'test_techcorp',
            'company_name': 'TechCorp Solutions',
            'industry': 'technology',
            'location': 'New York, USA',
            'employee_size': '201-500'
        },
        {
            'username': 'test_fintech',
            'company_name': 'FinTech Innovations',
            'industry': 'finance',
            'location': 'San Francisco, USA',
            'employee_size': '51-200'
        },
        {
            'username': 'test_healthmd',
            'company_name': 'HealthMD Inc',
            'industry': 'healthcare',
            'location': 'Boston, USA',
            'employee_size': '101-500'
        }
    ]
    
    for company in companies:
        user = User.objects.create_user(
            username=company['username'],
            email=f"{company['username']}@company.com",
            password='hr123456',
            first_name=company['company_name'].split()[0],
            last_name='HR'
        )
        
        # Create hr relationship
        hr.objects.create(user=user)
        
        # Create HRProfile
        HRProfile.objects.create(
            user=user,
            company_name=company['company_name'],
            industry=company['industry'],
            employee_size=company['employee_size'],
            location=company['location'],
            email=user.email,
            about_company=f"{company['company_name']} is a leading company in {company['industry']}.",
            website='https://example.com',
            linkedin_url='https://linkedin.com/company/example',
            twitter_url='https://twitter.com/example'
        )
        
        # Create status record
        UserStatus.objects.create(user=user, status='active')
        
        hr_list.append(user)
        print(f"✓ HR user created: {company['username']} ({company['company_name']})")
    
    return hr_list

def create_candidates():
    """Create candidate users"""
    print("\nCreating candidate users...")
    candidate_list = []
    
    candidates_data = [
        {'username': 'test_john_doe', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'test_jane_smith', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'test_mike_wilson', 'first_name': 'Mike', 'last_name': 'Wilson'},
        {'username': 'test_sarah_johnson', 'first_name': 'Sarah', 'last_name': 'Johnson'},
        {'username': 'test_alex_brown', 'first_name': 'Alex', 'last_name': 'Brown'},
    ]
    
    for candidate in candidates_data:
        user = User.objects.create_user(
            username=candidate['username'],
            email=f"{candidate['username']}@candidate.com",
            password='candidate123',
            first_name=candidate['first_name'],
            last_name=candidate['last_name']
        )
        
        # Create CandidateProfile
        CandidateProfile.objects.create(
            user=user,
            description=f"{candidate['first_name']} is a talented professional seeking new opportunities.",
            skills="Python, Django, React, SQL, API Development",
            languages="English, Spanish"
        )
        
        # Create status record
        UserStatus.objects.create(user=user, status='active')
        
        candidate_list.append(user)
        print(f"✓ Candidate user created: {candidate['username']}")
    
    return candidate_list

def create_job_posts(hr_users):
    """Create job posts"""
    print("\nCreating job posts...")
    jobs = [
        {
            'user': hr_users[0],  # TechCorp
            'title': 'Senior Python Developer',
            'description': 'We are looking for an experienced Python developer...',
            'address': 'New York, USA',
            'company': 'TechCorp Solutions',
            'salary_low': 100000,
            'salary_high': 150000,
            'employment_type': 'full-time',
            'work_mode': 'hybrid'
        },
        {
            'user': hr_users[0],
            'title': 'Junior Django Developer',
            'description': 'Entry-level Django developer position...',
            'address': 'New York, USA',
            'company': 'TechCorp Solutions',
            'salary_low': 60000,
            'salary_high': 80000,
            'employment_type': 'full-time',
            'work_mode': 'remote'
        },
        {
            'user': hr_users[1],  # FinTech
            'title': 'Frontend React Developer',
            'description': 'Join our fintech team as a React developer...',
            'address': 'San Francisco, USA',
            'company': 'FinTech Innovations',
            'salary_low': 120000,
            'salary_high': 160000,
            'employment_type': 'full-time',
            'work_mode': 'on-site'
        },
        {
            'user': hr_users[2],  # HealthMD
            'title': 'Healthcare Data Analyst',
            'description': 'Analyze healthcare data and provide insights...',
            'address': 'Boston, USA',
            'company': 'HealthMD Inc',
            'salary_low': 70000,
            'salary_high': 95000,
            'employment_type': 'full-time',
            'work_mode': 'hybrid'
        },
    ]
    
    for job in jobs:
        jb = JobPost.objects.create(
            user=job['user'],
            title=job['title'],
            address=job['address'],
            CompanyName=job['company'],
            salaryLow=job['salary_low'],
            salaryHigh=job['salary_high'],
            employment_type=job['employment_type'],
            work_mode=job['work_mode'],
            lastDateToApply=datetime.now().date() + timedelta(days=30)
        )
        print(f"✓ Job post created: {job['title']} ({job['company']})")
    
    return JobPost.objects.all()

def create_applications(candidates, job_posts):
    """Create candidate applications"""
    print("\nCreating applications...")
    
    # Create applications for first 3 candidates on all jobs
    for i, candidate in enumerate(candidates[:3]):
        for job in job_posts:
            try:
                candidateApplication.objects.create(
                    user=candidate,
                    job=job,
                    education_level='BACHELOR',
                    passingYear='2022',
                    yearOfExp=2,
                    status='pending'
                )
                print(f"✓ Application created: {candidate.username} → {job.title}")
            except:
                pass  # Skip if application already exists

def run():
    """Run all population functions"""
    print("=" * 60)
    print("JobPortal Test Data Population Script")
    print("=" * 60)
    
    try:
        clear_existing_data()
        admin = create_admin()
        hr_users = create_hr_users()
        candidates = create_candidates()
        job_posts = create_job_posts(hr_users)
        create_applications(candidates, job_posts)
        
        print("\n" + "=" * 60)
        print("✓ Test data population completed successfully!")
        print("=" * 60)
        print("\nLogin Credentials:")
        print("-" * 60)
        print("Admin Account:")
        print("  Username: admin_user")
        print("  Password: admin123")
        print("  Access: /admin_panel/")
        print("\nHR Accounts:")
        print("  Username: test_techcorp, test_fintech, test_healthmd")
        print("  Password: hr123456 (for all)")
        print("\nCandidate Accounts:")
        print("  Username: test_john_doe, test_jane_smith, test_mike_wilson, etc.")
        print("  Password: candidate123 (for all)")
        print("-" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during population: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    run()
