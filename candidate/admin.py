from django.contrib import admin
from candidate import models

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
class MyApplyJobListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job", "dateYouApply")
    list_filter = ('dateYouApply',)
    search_fields = ('user__username',)
    readonly_fields = ('dateYouApply',)
    ordering = ('-dateYouApply',)
    
    actions = ['delete_entire_candidate_database']
    
    def delete_entire_candidate_database(self, request, queryset):
        """Delete all Candidate-related data from the entire database"""
        profile_count = models.CandidateProfile.objects.all().count()
        apply_count = models.MyApplyJobList.objects.all().count()
        shortlist_count = models.IsShortlisted.objects.all().count()
        
        # Delete all Candidate-side data
        models.IsShortlisted.objects.all().delete()
        models.MyApplyJobList.objects.all().delete()
        models.CandidateProfile.objects.all().delete()
        
        self.message_user(
            request, 
            f'Successfully deleted ENTIRE CANDIDATE DATABASE: {profile_count} Profiles, '
            f'{apply_count} Apply Lists, {shortlist_count} Shortlisted entries.'
        )
    
    delete_entire_candidate_database.short_description = "DELETE ENTIRE CANDIDATE DATABASE (ALL CANDIDATE DATA)"


@admin.register(models.IsShortlisted)
class IsShortlistedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job", "shortlisted_date", "notification_read")
    list_filter = ('shortlisted_date', 'notification_read')
    search_fields = ('user__username', 'job__title')
    readonly_fields = ('shortlisted_date',)
    ordering = ('-shortlisted_date',)
