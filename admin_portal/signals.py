from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from hr.models import JobPost
from admin_portal.models import AdminActivityLog, AdminUser, JobPostModeration, UserStatus
from authuser.models import UserProfile


@receiver(post_save, sender=User)
def create_user_status_on_user_creation(sender, instance, created, **kwargs):
    """Automatically create UserStatus when a new user is registered"""
    if created:
        try:
            # Only create if UserProfile exists and user is not admin
            profile = instance.profile
            if profile.user_type in ['candidate', 'hr']:
                UserStatus.objects.get_or_create(
                    user=instance,
                    defaults={
                        'user_type': profile.user_type,
                        'status': 'active'
                    }
                )
        except UserProfile.DoesNotExist:
            pass


@receiver(post_save, sender=JobPost)
def create_job_post_moderation(sender, instance, created, **kwargs):
    """Automatically create JobPostModeration record when job is posted"""
    if created:
        try:
            # Check if admin exists for the HR user
            admin_user = AdminUser.objects.filter(user=instance.user).first()
            JobPostModeration.objects.get_or_create(
                job_post=instance,
                defaults={
                    'status': 'approved',  # Auto-approve unless flagged
                    'moderated_by': admin_user,
                }
            )
        except Exception as e:
            print(f"Error creating JobPostModeration: {e}")


def log_admin_activity(admin_user, action_type, description, target_user=None):
    """Helper function to log admin activities"""
    try:
        AdminActivityLog.objects.create(
            admin=admin_user,
            action_type=action_type,
            description=description,
            target_user=target_user
        )
    except Exception as e:
        print(f"Error logging admin activity: {e}")
