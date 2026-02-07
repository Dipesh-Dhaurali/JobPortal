from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date


# -------------------------------
# Recruiter / HR Account
# -------------------------------
class hr(models.Model):
    """Recruiter/HR account linked with Django User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Recruiter Account"
        verbose_name_plural = "Recruiter Accounts"

    def __str__(self):
        return f"{self.user.username} (Recruiter)"


# -------------------------------
# Choice Constants
# -------------------------------
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

EXPERIENCE_LEVEL_CHOICES = (
    ('no-experience', 'No experience required'),
    ('6-months', '6 months'),
    ('1-year', '1 year'),
    ('2-years', '2 years'),
    ('3-years', '3 years'),
    ('4-years', '4 years'),
    ('5-plus-years', '5+ years'),
    ('others', 'Others'),
)

REQUIRED_EDUCATION_CHOICES = (
    ('no-education', 'No education required'),
    ('see', 'SEE'),
    ('slc', 'SLC'),
    ('plus2', '+2'),
    ('diploma', 'Diploma'),
    ('bachelor', 'Bachelor'),
    ('master', 'Master'),
    ('phd', 'PhD'),
)


# -------------------------------
# Job Post Model
# -------------------------------
class JobPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    CompanyName = models.CharField(max_length=200)
    salaryLow = models.FloatField(default=0, validators=[MinValueValidator(0)])
    salaryHigh = models.FloatField(default=0, validators=[MinValueValidator(0)])
    applycount = models.IntegerField(default=0)
    lastDateToApply = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    employment_type = models.CharField(
        max_length=20, choices=EMPLOYMENT_TYPE_CHOICES,
        default='full-time', null=True, blank=True
    )
    work_mode = models.CharField(
        max_length=20, choices=WORK_MODE_CHOICES,
        default='on-site', null=True, blank=True
    )

    required_experience = models.CharField(
        max_length=50,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='no-experience',
        help_text='Select required years of experience'
    )
    required_experience_custom = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Custom experience requirement (e.g., 1.5 years)'
    )
    required_education = models.CharField(
        max_length=50,
        choices=REQUIRED_EDUCATION_CHOICES,
        default='no-education',
        help_text='Select required education level'
    )
    required_skills = models.TextField(
        null=True,
        blank=True,
        help_text='Comma-separated skills (e.g., Python, SQL, Communication)'
    )

    def clean(self):
        errors = {}

        if self.salaryLow > 0 and self.salaryHigh > 0:
            if self.salaryHigh <= self.salaryLow:
                errors['salaryHigh'] = "Maximum salary must be greater than minimum salary."

        if self.lastDateToApply < date.today():
            errors['lastDateToApply'] = "Application deadline cannot be in the past."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_required_experience_display(self):
        if self.required_experience == 'others':
            return self.required_experience_custom
        return dict(EXPERIENCE_LEVEL_CHOICES).get(self.required_experience)

    def get_required_education_display(self):
        return dict(REQUIRED_EDUCATION_CHOICES).get(self.required_education)

    def get_required_skills_list(self):
        if self.required_skills:
            return [s.strip() for s in self.required_skills.split(',') if s.strip()]
        return []

    def __str__(self):
        return self.title


# -------------------------------
# Shortlisted Candidate
# -------------------------------
class ShortlistedCandidate(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate = models.OneToOneField(
        'candidate.candidateApplication',
        on_delete=models.CASCADE
    )
    shortlisted_at = models.DateTimeField(auto_now_add=True, null=True)
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.candidate.user.username} shortlisted for {self.job.title}"


# -------------------------------
# Selected Candidate
# -------------------------------
class SelectedCandidate(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate = models.OneToOneField(
        'candidate.candidateApplication',
        on_delete=models.CASCADE
    )
    selected_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.candidate.user.username} selected for {self.job.title}"


# -------------------------------
# Recruiter Profile (RENAMED SAFELY)
# -------------------------------
class RecruiterProfile(models.Model):
    """Recruiter / Company profile (Renamed from HRProfile safely)"""

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

    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_hrprofile'
        verbose_name = "Recruiter Profile"
        verbose_name_plural = "Recruiter Profiles"

    def __str__(self):
        return f"{self.company_name} - {self.user.username}"
