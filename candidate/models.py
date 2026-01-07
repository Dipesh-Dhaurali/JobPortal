from django.db import models
from django.contrib.auth.models import User
from hr.models import candidateApplication, JobPost

# Create your candidate models here.

class MyApplyJobList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.OneToOneField(candidateApplication,on_delete=models.CASCADE)
    dateYouApply=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.job.job.title}"

class IsShortlisted(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job=models.ForeignKey(JobPost,on_delete=models.CASCADE)
    shortlisted_date=models.DateField(auto_now_add=True)
    notification_read=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'job')
    
    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

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
        ('gpa', 'GPA (out of 10)'),
        ('percentage', 'Percentage (out of 100)'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.FileField(upload_to='candidate_photos/', null=True, blank=True)
    job_preference_title = models.CharField(max_length=200, help_text="e.g., Document Officer")
    preferred_job_level = models.CharField(max_length=20, choices=JOB_LEVEL_CHOICES)
    preferred_job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    work_experience = models.IntegerField(default=0)
    
    # Education fields
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    course_or_program = models.CharField(max_length=200, help_text="e.g., BIM")
    gpa_percentage_type = models.CharField(max_length=10, choices=GPA_PERCENTAGE_CHOICES)
    gpa_percentage_value = models.FloatField()
    school_college_name = models.CharField(max_length=200)
    graduation_year = models.IntegerField()
    
    # Skills and languages
    skills = models.TextField(help_text="e.g., Public Speaking, Computer Operation")
    languages = models.TextField(help_text="e.g., Nepali, English")
    
    # Social media accounts
    social_account_name_1 = models.CharField(max_length=100, null=True, blank=True)
    social_account_url_1 = models.URLField(null=True, blank=True)
    social_account_name_2 = models.CharField(max_length=100, null=True, blank=True)
    social_account_url_2 = models.URLField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
