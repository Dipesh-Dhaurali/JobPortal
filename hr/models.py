from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

class hr(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username

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

    def __str__(self):
        return str(self.title)
    

STATUS_CHOICE=(
    ('pending','pending'),
    ('shortlisted','shortlisted'),
    ('rejected','rejected'),
    ('selected','selected'), # Added selected status for final candidate selection
)

EDUCATION_CHOICES = (
    ('SEE', 'SEE (School Leaving Exam)'),
    ('SLC', 'SLC (School Leaving Certificate)'),
    ('PLUS2', '+2 (Higher Secondary)'),
    ('DIPLOMA', 'Diploma'),
    ('BACHELOR', 'Bachelor'),
    ('MASTERS', 'Masters'),
)

class candidateApplication(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost,on_delete=models.CASCADE)
    education_level = models.CharField(
        max_length=20, 
        choices=EDUCATION_CHOICES, 
        default='BACHELOR'
    )
    passingYear=models.IntegerField()
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
            'SEE': 'SEE (School Leaving Exam)',
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
