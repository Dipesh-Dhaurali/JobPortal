from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile for tracking user type and additional info"""
    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('hr', 'HR/Company'),
        ('admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Type & Verification"
        verbose_name_plural = "User Types & Verification"
    
    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
