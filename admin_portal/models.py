from django.db import models
from django.contrib.auth.models import User
from hr.models import hr, JobPost
from candidate.models import CandidateProfile

class AdminUser(models.Model):
    """Admin user model to manage platform administrators"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_super_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Admin User"
        verbose_name_plural = "Admin Users"
    
    def __str__(self):
        return f"Admin - {self.user.username}"


class UserStatus(models.Model):
    """Track the status of HR and Candidate accounts"""
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Review'),
    )
    
    USER_TYPE_CHOICES = (
        ('hr', 'HR/Company'),
        ('candidate', 'Candidate'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    reason_for_suspension = models.TextField(null=True, blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    suspended_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='suspended_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Account Status"
        verbose_name_plural = "User Account Statuses"
    
    def __str__(self):
        return f"{self.user.username} - {self.status}"


class JobPostModeration(models.Model):
    """Track moderation actions on job posts"""
    ACTION_CHOICES = (
        ('flagged', 'Flagged for Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('edited', 'Edited'),
        ('deleted', 'Deleted'),
    )
    
    job_post = models.OneToOneField(JobPost, on_delete=models.CASCADE, related_name='moderation')
    status = models.CharField(max_length=20, choices=ACTION_CHOICES, default='flagged')
    reason = models.TextField(null=True, blank=True)
    moderated_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True, blank=True)
    moderated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Job Post Moderation"
        verbose_name_plural = "Job Post Moderations"
    
    def __str__(self):
        return f"{self.job_post.title} - {self.status}"


class AdminActivityLog(models.Model):
    """Log all admin actions for audit trail"""
    ACTION_TYPES = (
        ('user_suspended', 'User Suspended'),
        ('user_activated', 'User Activated'),
        ('job_approved', 'Job Approved'),
        ('job_rejected', 'Job Rejected'),
        ('job_deleted', 'Job Deleted'),
        ('job_edited', 'Job Edited'),
        ('profile_viewed', 'Profile Viewed'),
    )
    
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    description = models.TextField()
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='admin_actions')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Admin Activity Log"
        verbose_name_plural = "Admin Activity Logs"
        ordering = ('-created_at',)
    
    def __str__(self):
        return f"{self.admin.user.username} - {self.action_type}"
