from django.contrib import admin
from candidate import models

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
