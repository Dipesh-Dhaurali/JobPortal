from django.contrib import admin
from django.core.exceptions import ValidationError
from hr import models

# Register your models here.

@admin.register(models.hr)
class RecruiterAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_user_email')
    search_fields = ('user__username', 'user__email')
    ordering = ('-id',)
    
    def get_queryset(self, request):
        """Ensure all recruiter accounts are returned, including old records"""
        return super().get_queryset(request).select_related('user').order_by('-id')
    
    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Email'
    
    actions = ['delete_entire_recruiter_database']
    
    def delete_entire_recruiter_database(self, request, queryset):
        """Delete all recruiter/HR-related data from the entire database"""
        recruiter_count = models.hr.objects.all().count()
        job_count = models.JobPost.objects.all().count()
        app_count = models.candidateApplication.objects.all().count()
        shortlist_count = models.ShortlistedCandidate.objects.all().count()
        
        # Delete all recruiter-side data
        models.ShortlistedCandidate.objects.all().delete()
        models.candidateApplication.objects.all().delete()
        models.JobPost.objects.all().delete()
        models.hr.objects.all().delete()
        
        self.message_user(
            request, 
            f'Successfully deleted ENTIRE RECRUITER DATABASE: {recruiter_count} Recruiters, {job_count} Job Posts, '
            f'{app_count} Applications, {shortlist_count} Shortlisted entries.'
        )
    
    delete_entire_recruiter_database.short_description = "DELETE ENTIRE RECRUITER DATABASE (ALL RECRUITER DATA)"


@admin.register(models.JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'address', 'CompanyName',
                    'salaryLow', 'salaryHigh', 'applycount', 'lastDateToApply', 'created_at')
    list_filter = ('lastDateToApply', 'created_at', 'CompanyName')
    search_fields = ('title', 'CompanyName', 'address')
    readonly_fields = ('applycount', 'created_at')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        """Ensure all job posts are returned, including old records"""
        return super().get_queryset(request).select_related('user').order_by('-created_at')
    
    fieldsets = (
        ('Job Information', {
            'fields': ('user', 'title', 'address', 'CompanyName')
        }),
        ('Salary Details', {
            'fields': ('salaryLow', 'salaryHigh'),
            'description': 'Maximum salary must be greater than minimum salary.'
        }),
        ('Job Type & Mode', {
            'fields': ('employment_type', 'work_mode')
        }),
        ('Application Details', {
            'fields': ('lastDateToApply', 'applycount'),
            'description': 'Application deadline must be today or a future date.'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['delete_all_job_posts']
    
    def delete_all_job_posts(self, request, queryset):
        """Delete all job posts in the database"""
        total_count = models.JobPost.objects.all().count()
        models.JobPost.objects.all().delete()
        self.message_user(request, f'Successfully deleted all {total_count} job posts.')
    
    delete_all_job_posts.short_description = "Delete ALL Job Posts (entire database)"
    
    def save_model(self, request, obj, form, change):
        """Override save_model to catch and display validation errors"""
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
            self.message_user(request, f"Job post '{obj.title}' saved successfully.")
        except ValidationError as e:
            # Display validation errors to the user
            for field, error in e.error_dict.items():
                form.add_error(field, error[0].message if hasattr(error[0], 'message') else str(error[0]))
            raise


# candidateApplication is now registered in candidate/admin.py
# This ensures all candidate-related data is managed in the Candidate section of Admin


@admin.register(models.ShortlistedCandidate)
class ShortlistedCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'candidate', 'shortlisted_at', 'notification_sent')
    list_filter = ('shortlisted_at', 'notification_sent')
    search_fields = ('job__title', 'candidate__user__username')
    readonly_fields = ('shortlisted_at',)
    ordering = ('-shortlisted_at',)
    
    def get_queryset(self, request):
        """Ensure all shortlisted candidates are returned, including old records"""
        return super().get_queryset(request).select_related('job', 'candidate').order_by('-shortlisted_at')


@admin.register(models.SelectedCandidate)
class SelectedCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'candidate', 'selected_at')
    list_filter = ('selected_at',)
    search_fields = ('job__title', 'candidate__user__username')
    readonly_fields = ('selected_at',)
    ordering = ('-selected_at',)
    
    def get_queryset(self, request):
        """Ensure all selected candidates are returned, including old records"""
        return super().get_queryset(request).select_related('job', 'candidate').order_by('-selected_at')


@admin.register(models.HRProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    """Manage recruiter profiles - displays company and contact information"""
    list_display = ('id', 'user', 'company_name', 'industry', 'employee_size', 'created_at')
    list_filter = ('industry', 'company_type', 'employee_size', 'created_at')
    search_fields = ('user__username', 'company_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        """Ensure all recruiter profiles are returned, including old records"""
        return super().get_queryset(request).select_related('user').order_by('-created_at')
    
    fieldsets = (
        ('Company Info', {
            'fields': ('user', 'company_name', 'company_logo', 'cover_image', 'company_type')
        }),
        ('Company Details', {
            'fields': ('industry', 'employee_size', 'location', 'about_company')
        }),
        ('Contact Info', {
            'fields': ('email', 'phone_number', 'website')
        }),
        ('Social Media', {
            'fields': ('linkedin_url', 'facebook_url', 'twitter_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
