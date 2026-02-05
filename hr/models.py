from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

class hr(models.Model):
    """Recruiter/HR profile - Represents a company or HR person managing job postings"""
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Recruiter Account"
        verbose_name_plural = "Recruiter Accounts"
    
    def __str__(self):
        return f"{self.user.username} (Recruiter)"

EMPLOYMENT_TYPE_CHOICES = (
    ('full-time', 'Full-time'),
    ('part-time', 'Part-time'),
    ('internship', 'Internship'),
    ('contract', 'Contract'),
    ('freelance', 'Freelance'),
)

WORK_MODE_CHOICES = (
    ('on-site', 'On-site'),
    ('remote', 'Remote'),
    ('hybrid', 'Hybrid'),
)

class JobPost(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    CompanyName=models.CharField(max_length=200)
    salaryLow=models.FloatField(default=0, validators=[MinValueValidator(0)])
    salaryHigh=models.FloatField(default=0, validators=[MinValueValidator(0)])
    applycount=models.IntegerField(default=0)
    lastDateToApply=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full-time', null=True, blank=True)
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='on-site', null=True, blank=True)

    def clean(self):
        """Validate salary range and application deadline"""
        errors = {}
        
        # Validate salary range: max must be greater than min
        if self.salaryLow > 0 and self.salaryHigh > 0:
            if self.salaryHigh <= self.salaryLow:
                errors['salaryHigh'] = "Maximum salary must be greater than minimum salary."
        
        # Validate application deadline: must be today or later
        if self.lastDateToApply < date.today():
            errors['lastDateToApply'] = "Application deadline cannot be in the past. Please select today or a future date."
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        """Call clean before saving"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
    

STATUS_CHOICE=(
    ('pending','pending'),
    ('shortlisted','shortlisted'),
    ('rejected','rejected'),
    ('selected','selected'), # Added selected status for final candidate selection
)

EDUCATION_CHOICES = (
    ('SEE', 'SEE (Secondary Education Examination)'),  # Updated full form from School Leaving Exam to Secondary Education Examination
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
            'SEE': 'SEE (Secondary Education Examination)',  # Updated to match the corrected full form
            'SLC': 'SLC (School Leaving Certificate)',
            'PLUS2': '+2 (Higher Secondary)',
            'DIPLOMA': 'Diploma',
            'BACHELOR': 'Bachelor',
            'MASTERS': 'Masters',
        }
        return education_map.get(self.education_level, self.education_level)

class ShortlistedCandidate(models.Model):
    job=models.ForeignKey(JobPost,on_delete=models.CASCADE)
    candidate=models.OneToOneField(candidateApplication,on_delete=models.CASCADE)
    shortlisted_at=models.DateTimeField(auto_now_add=True, null=True)
    notification_sent=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.candidate.user.username} shortlisted for {self.job.title}"

class SelectedCandidate(models.Model):
    job=models.ForeignKey(JobPost,on_delete=models.CASCADE)
    candidate=models.OneToOneField(candidateApplication,on_delete=models.CASCADE)
    selected_at=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.candidate.user.username} selected for {self.job.title}"

class HRProfile(models.Model):
    """HR/Company profile model for storing company information"""
    INDUSTRY_CHOICES = (
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('education', 'Education'),
        ('hospitality', 'Hospitality'),
        ('real_estate', 'Real Estate'),
        ('banking', 'Banking'),
        ('insurance', 'Insurance'),
        ('consulting', 'Consulting'),
        ('logistics', 'Logistics'),
        ('media', 'Media & Entertainment'),
        ('other', 'Other'),
    )
    
    EMPLOYEE_SIZE_CHOICES = (
        ('1-10', '1 - 10 employees'),
        ('11-50', '11 - 50 employees'),
        ('51-200', '51 - 200 employees'),
        ('201-500', '201 - 500 employees'),
        ('501-1000', '501 - 1000 employees'),
        ('1000+', '1000+ employees'),
    )
    
    COMPANY_TYPE_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public'),
        ('ngo', 'NGO'),
        ('startup', 'Startup'),
        ('government', 'Government'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='hr_logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='hr_covers/', null=True, blank=True)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES, default='private')
    employee_size = models.CharField(max_length=20, choices=EMPLOYEE_SIZE_CHOICES)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200)
    about_company = models.TextField(help_text="Describe your company")
    
    # Social Media
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.user.username}"
