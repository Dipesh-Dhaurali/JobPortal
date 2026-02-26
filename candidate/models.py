from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from hr.models import JobPost


class CandidateAccount(models.Model):
    """Track all registered candidate accounts with status and management"""
    ACCOUNT_STATUS_CHOICES = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Verification'),
        ('inactive', 'Inactive'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_account')
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='active')
    reason_for_suspension = models.TextField(null=True, blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspended_by = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Candidate Account"
        verbose_name_plural = "Candidate Accounts"
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.user.username} - {self.account_status}"


STATUS_CHOICE=(
    ('pending','pending'),
    ('shortlisted','shortlisted'),
    ('rejected','rejected'),
    ('selected','selected'), # Added selected status for final candidate selection
)

EDUCATION_CHOICES = (
    ('SEE', 'SEE (Secondary Education Examination)'),  
    ('SLC', 'SLC (School Leaving Certificate)'),
    ('PLUS2', '+2 (Higher Secondary)'),
    ('DIPLOMA', 'Diploma'),
    ('BACHELOR', 'Bachelor'),
    ('MASTERS', 'Masters'),
)

PASSING_YEAR_CHOICES = (
    ('currently_running', 'Currently Running'),
) + tuple((str(year), str(year)) for year in range(2030, 1989, -1))

class candidateApplication(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost,on_delete=models.CASCADE)
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_CHOICES, 
        default='BACHELOR'
    )
    passingYear = models.CharField(
        max_length=20,
        choices=PASSING_YEAR_CHOICES,
        default='currently_running'
    )
    yearOfExp=models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    resume=models.FileField(upload_to="resume")
    support_documents=models.FileField(
        upload_to="support_docs",
        null=True,
        blank=True,
        help_text="Optional: Academic documents (PDF only, max 5MB)"
    )
    status=models.CharField(choices=STATUS_CHOICE, default="pending", max_length=20)
    applied_at=models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        unique_together = ('user', 'job')
    
    def __str__(self):
        return f"{self.user.username} - {self.job.title}"
    
    def get_education_display(self):
        education_map = {
            'SEE': 'SEE (Secondary Education Examination)', 
            'SLC': 'SLC (School Leaving Certificate)',
            'PLUS2': '+2 (Higher Secondary)',
            'DIPLOMA': 'Diploma',
            'BACHELOR': 'Bachelor',
            'MASTERS': 'Masters',
        }
        return education_map.get(self.education_level, self.education_level)

class MyApplyJobList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.OneToOneField(candidateApplication,on_delete=models.CASCADE)
    dateYouApply=models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Job Application Tracker"
        verbose_name_plural = "Job Application Trackers"
    
    def __str__(self):
        try:
            return f"{self.user.username} - {self.job.job.title}"
        except Exception:
            return f"{self.user_id} - Application"

class CandidateProfile(models.Model):
    JOB_LEVEL_CHOICES = (
        ('top', 'Top Level'),
        ('senior', 'Senior Level'),
        ('mid', 'Mid Level'),
        ('junior', 'Junior/Entry Level'),
        ('internship', 'Internship'),
    )
    
    JOB_TYPE_CHOICES = (
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
    )
    
    EDUCATION_CHOICES = (
        ('see', 'SEE (Secondary Education Examination)'),
        ('slc', 'SLC (School Leaving Certificate)'),
        ('plus2', '+2 (Higher Secondary)'),
        ('diploma', 'Diploma'),
        ('bachelor', 'Bachelor'),
        ('masters', 'Masters'),
    )
    
    GPA_PERCENTAGE_CHOICES = (
        ('gpa_4', 'GPA (out of 4)'),
        ('gpa_10', 'GPA (out of 10)'),
        ('percentage', 'Percentage (out of 100)'),
    )
    
    PREFERRED_INDUSTRY_CHOICES = (
        ('it', 'IT'),
        ('fintech', 'FinTech'),
        ('ecommerce', 'E-Commerce'),
        ('healthcare', 'Healthcare'),
        ('banking_finance', 'Banking & Finance'),
        ('education', 'Education'),
        ('telecommunications', 'Telecommunications'),
        ('manufacturing', 'Manufacturing'),
        ('engineering', 'Engineering'),
        ('digital_marketing', 'Digital Marketing'),
        ('management', 'Management / Managers'),
        ('real_estate', 'Real Estate'),
        ('insurance', 'Insurance'),
    )
    
    GRADUATION_YEAR_CHOICES = (
        ('currently_running', 'Currently Running'),
    ) + tuple((str(year), str(year)) for year in range(2030, 1899, -1))
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='candidate_photos/', null=True, blank=True)
    job_preference_title = models.CharField(max_length=200, help_text="e.g., Document Officer")
    preferred_job_level = models.CharField(max_length=20, choices=JOB_LEVEL_CHOICES)
    preferred_job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_experience = models.IntegerField(default=0)
    
    # Additional job interest & experience details
    job_interest = models.TextField(
        null=True,
        blank=True,
        help_text="Job interests as comma-separated text, e.g., Software Developer, Data Analyst",
    )
    work_experience_description = models.TextField(
        null=True,
        blank=True,
        help_text="Brief description of your work experience",
    )
    preferred_industry = models.CharField(
        max_length=50,
        choices=PREFERRED_INDUSTRY_CHOICES,
        null=True,
        blank=True,
    )
    
    # Education fields
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    course_or_program = models.CharField(max_length=200, help_text="e.g., BIM")
    gpa_percentage_type = models.CharField(max_length=10, choices=GPA_PERCENTAGE_CHOICES)
    gpa_percentage_value = models.FloatField()
    school_college_name = models.CharField(max_length=200)
    graduation_year = models.CharField(
        max_length=20, 
        choices=GRADUATION_YEAR_CHOICES,
        default='currently_running'
    )
    
    # Skills and languages
    skills = models.TextField(help_text="e.g., Public Speaking, Computer Operation")
    languages = models.TextField(help_text="e.g., Nepali, English")
    
    # Career summary / mini bio
    career_summary = models.TextField(
        null=True,
        blank=True,
        help_text="Short career summary / mini bio",
    )
    
    # Social media accounts
    social_account_name_1 = models.CharField(max_length=100, null=True, blank=True)
    social_account_url_1 = models.URLField(null=True, blank=True)
    social_account_name_2 = models.CharField(max_length=100, null=True, blank=True)
    social_account_url_2 = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
