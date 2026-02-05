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


@admin.register(models.MyApplyJobList)
class JobApplicationTrackerAdmin(admin.ModelAdmin):
    """Tracks all job applications submitted by candidates"""
    list_display = ("id", "user", "job", "dateYouApply")
    list_filter = ('dateYouApply',)
    search_fields = ('user__username', 'job__job__title')
    readonly_fields = ('dateYouApply',)
    ordering = ('-dateYouApply',)
    
    fieldsets = (
        ('Application Info', {
            'fields': ('user', 'job')
        }),
        ('Application Date', {
            'fields': ('dateYouApply',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - only auto-created when candidate applies"""
        return False
    
    actions = ['delete_entire_candidate_database']
    
    def delete_entire_candidate_database(self, request, queryset):
        """Delete all Candidate-related data from the entire database"""
        profile_count = models.CandidateProfile.objects.all().count()
        apply_count = models.MyApplyJobList.objects.all().count()
        account_count = models.CandidateAccount.objects.all().count()
        
        # Delete all Candidate-side data
        models.CandidateAccount.objects.all().delete()
        models.MyApplyJobList.objects.all().delete()
        models.CandidateProfile.objects.all().delete()
        
        self.message_user(
            request, 
            f'Successfully deleted ENTIRE CANDIDATE DATABASE: {profile_count} Profiles, '
            f'{apply_count} Apply Lists, {account_count} Candidate Accounts.'
        )
    
    delete_entire_candidate_database.short_description = "DELETE ENTIRE CANDIDATE DATABASE (ALL CANDIDATE DATA)"


# Shortlist Notifications removed - use HR app's ShortlistedCandidate model instead
