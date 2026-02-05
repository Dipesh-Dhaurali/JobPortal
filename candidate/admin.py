from django.contrib import admin
from candidate import models

@admin.register(models.CandidateAccount)
class CandidateAccountAdmin(admin.ModelAdmin):
    """Manage all registered candidate accounts with suspend/delete functionality"""
    list_display = ('id', 'user', 'account_status', 'created_at', 'suspended_at')
    list_filter = ('account_status', 'created_at', 'suspended_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'suspended_at')
    
    fieldsets = (
        ('Account Info', {
            'fields': ('user', 'account_status')
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
    
    actions = ['mark_active', 'mark_suspended', 'mark_pending']
    
    def mark_active(self, request, queryset):
        """Mark selected accounts as active"""
        updated = queryset.update(account_status='active', suspended_at=None)
        self.message_user(request, f"Activated {updated} candidate account(s).")
    mark_active.short_description = "Mark as Active"
    
    def mark_suspended(self, request, queryset):
        """Mark selected accounts as suspended"""
        updated = queryset.update(account_status='suspended')
        self.message_user(request, f"Suspended {updated} candidate account(s).")
    mark_suspended.short_description = "Mark as Suspended"
    
    def mark_pending(self, request, queryset):
        """Mark selected accounts as pending verification"""
        updated = queryset.update(account_status='pending')
        self.message_user(request, f"Marked {updated} candidate account(s) as pending verification.")
    mark_pending.short_description = "Mark as Pending Verification"


@admin.register(models.CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job_preference_title', 'preferred_job_level', 'education_level', 'created_at')
    list_filter = ('preferred_job_level', 'preferred_job_type', 'education_level', 'created_at')
    search_fields = ('user__username', 'user__email', 'job_preference_title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'profile_photo', 'job_preference_title')
        }),
        ('Job Preferences', {
            'fields': ('preferred_job_level', 'preferred_job_type', 'work_experience')
        }),
        ('Education', {
            'fields': ('education_level', 'course_or_program', 'school_college_name', 'graduation_year', 'gpa_percentage_type', 'gpa_percentage_value')
        }),
        ('Skills & Languages', {
            'fields': ('skills', 'languages')
        }),
        ('Social Accounts', {
            'fields': ('social_account_name_1', 'social_account_url_1', 'social_account_name_2', 'social_account_url_2'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Job Application Tracker is registered in hr/admin.py as candidateApplicationAdmin
# Shortlist Notifications are managed through HR app's ShortlistedCandidate model
