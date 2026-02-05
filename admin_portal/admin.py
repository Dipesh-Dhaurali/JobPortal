from django.contrib import admin
from .models import AdminUser, UserStatus, JobPostModeration, AdminActivityLog

@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    """Grant admin privileges to specific users"""
    list_display = ('user', 'is_super_admin', 'created_at')
    list_filter = ('is_super_admin', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Admin User Info', {
            'fields': ('user', 'is_super_admin'),
            'description': 'Select user to grant admin privileges. Super admin has all permissions.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    """Manage candidate and HR account statuses (active/suspended/pending)"""
    list_display = ('user', 'user_type', 'status', 'suspended_at')
    list_filter = ('status', 'user_type')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'suspended_at')
    
    fieldsets = (
        ('User Status Info', {
            'fields': ('user', 'user_type', 'status')
        }),
        ('Suspension Details', {
            'fields': ('reason_for_suspension', 'suspended_by', 'suspended_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_active', 'mark_suspended']
    
    def mark_active(self, request, queryset):
        """Mark selected users as active"""
        updated = queryset.update(status='active', suspended_at=None)
        self.message_user(request, f"Activated {updated} user(s).")
    mark_active.short_description = "Mark selected users as Active"
    
    def mark_suspended(self, request, queryset):
        """Mark selected users as suspended"""
        updated = queryset.update(status='suspended')
        self.message_user(request, f"Suspended {updated} user(s).")
    mark_suspended.short_description = "Mark selected users as Suspended"

@admin.register(JobPostModeration)
class JobPostModerationAdmin(admin.ModelAdmin):
    """Audit trail for job post moderation actions (approve/reject/edit/delete)"""
    list_display = ('job_post', 'status', 'moderated_by', 'moderated_at')
    list_filter = ('status', 'moderated_at')
    search_fields = ('job_post__title', 'reason', 'moderated_by__user__username')
    readonly_fields = ('moderated_at',)
    
    fieldsets = (
        ('Job Moderation Info', {
            'fields': ('job_post', 'status', 'moderated_by')
        }),
        ('Moderation Details', {
            'fields': ('reason', 'moderated_at')
        }),
    )
    
    actions = ['mark_approved', 'mark_rejected']
    
    def mark_approved(self, request, queryset):
        """Mark jobs as approved"""
        updated = queryset.update(status='approved')
        self.message_user(request, f"Approved {updated} job post(s).")
    mark_approved.short_description = "Mark jobs as Approved"
    
    def mark_rejected(self, request, queryset):
        """Mark jobs as rejected"""
        updated = queryset.update(status='rejected')
        self.message_user(request, f"Rejected {updated} job post(s).")
    mark_rejected.short_description = "Mark jobs as Rejected"

@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    """Complete audit trail of all admin actions for compliance and debugging"""
    list_display = ('admin', 'action_type', 'target_user', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('admin__user__username', 'target_user__username', 'description')
    readonly_fields = ('created_at', 'admin', 'action_type', 'description', 'target_user')
    
    fieldsets = (
        ('Admin Action Info', {
            'fields': ('admin', 'action_type', 'target_user')
        }),
        ('Action Description', {
            'fields': ('description',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - auto-created by signals"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion - maintain audit trail"""
        return False
