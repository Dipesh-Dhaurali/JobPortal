from django.contrib import admin
from .models import AdminUser, UserStatus, JobPostModeration, AdminActivityLog

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_super_admin', 'created_at')
    list_filter = ('is_super_admin', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'status', 'suspended_at')
    list_filter = ('status', 'user_type')
    search_fields = ('user__username', 'user__email')

@admin.register(JobPostModeration)
class JobPostModerationAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'status', 'moderated_at')
    list_filter = ('status',)
    search_fields = ('job_post__title',)

@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_type', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('admin__user__username', 'description')
    readonly_fields = ('created_at',)
