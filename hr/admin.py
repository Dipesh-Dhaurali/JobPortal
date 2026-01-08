from django.contrib import admin
from hr import models

# Register your models here.

@admin.register(models.hr)
class hrAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')
    
    actions = ['delete_entire_hr_database']
    
    def delete_entire_hr_database(self, request, queryset):
        """Delete all HR-related data from the entire database"""
        hr_count = models.hr.objects.all().count()
        job_count = models.JobPost.objects.all().count()
        app_count = models.candidateApplication.objects.all().count()
        shortlist_count = models.ShortlistedCandidate.objects.all().count()
        
        # Delete all HR-side data
        models.ShortlistedCandidate.objects.all().delete()
        models.candidateApplication.objects.all().delete()
        models.JobPost.objects.all().delete()
        models.hr.objects.all().delete()
        
        self.message_user(
            request, 
            f'Successfully deleted ENTIRE HR DATABASE: {hr_count} HRs, {job_count} Job Posts, '
            f'{app_count} Applications, {shortlist_count} Shortlisted entries.'
        )
    
    delete_entire_hr_database.short_description = "DELETE ENTIRE HR DATABASE (ALL HR DATA)"


@admin.register(models.JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'address', 'CompanyName',
                    'salaryLow', 'salaryHigh', 'applycount', 'lastDateToApply', 'created_at')
    list_filter = ('lastDateToApply', 'created_at', 'CompanyName')
    search_fields = ('title', 'CompanyName', 'address')
    readonly_fields = ('applycount', 'created_at')
    ordering = ('-created_at',)
    
    actions = ['delete_all_job_posts']
    
    def delete_all_job_posts(self, request, queryset):
        """Delete all job posts in the database"""
        total_count = models.JobPost.objects.all().count()
        models.JobPost.objects.all().delete()
        self.message_user(request, f'Successfully deleted all {total_count} job posts.')
    
    delete_all_job_posts.short_description = "Delete ALL Job Posts (entire database)"


@admin.register(models.candidateApplication)
class candidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'status', 'passingYear', 'yearOfExp', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__title')
    readonly_fields = ('applied_at',)
    ordering = ('-applied_at',)
    
    actions = ['delete_all_applications']
    
    def delete_all_applications(self, request, queryset):
        """Delete all candidate applications in the database"""
        total_count = models.candidateApplication.objects.all().count()
        models.candidateApplication.objects.all().delete()
        self.message_user(request, f'Successfully deleted all {total_count} candidate applications.')
    
    delete_all_applications.short_description = "Delete ALL Candidate Applications (entire database)"


@admin.register(models.ShortlistedCandidate)
class ShortlistedCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'candidate', 'shortlisted_at', 'notification_sent')
    list_filter = ('shortlisted_at', 'notification_sent')
    search_fields = ('job__title', 'candidate__user__username')
    readonly_fields = ('shortlisted_at',)
    ordering = ('-shortlisted_at',)
