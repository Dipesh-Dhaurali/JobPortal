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
