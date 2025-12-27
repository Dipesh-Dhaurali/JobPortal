from django.contrib import admin
from candidate import models

@admin.register(models.MyApplyJobList)
class MyApplyJobListAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job", "dateYouApply")
    list_filter = ('dateYouApply',)
    search_fields = ('user__username',)
    readonly_fields = ('dateYouApply',)
    ordering = ('-dateYouApply',)


@admin.register(models.IsShortlisted)
class IsShortlistedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job", "shortlisted_date", "notification_read")
    list_filter = ('shortlisted_date', 'notification_read')
    search_fields = ('user__username', 'job__title')
    readonly_fields = ('shortlisted_date',)
    ordering = ('-shortlisted_date',)
