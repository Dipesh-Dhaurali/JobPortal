from django.contrib import admin
from hr import models

# Register your models here.

@admin.register(models.hr)
class hrAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'user__email')


@admin.register(models.JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'address', 'CompanyName',
                    'salaryLow', 'salaryHigh', 'applycount', 'lastDateToApply', 'created_at')
    list_filter = ('lastDateToApply', 'created_at', 'CompanyName')
    search_fields = ('title', 'CompanyName', 'address')
    readonly_fields = ('applycount', 'created_at')
    ordering = ('-created_at',)


@admin.register(models.candidateApplication)
class candidateApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'job', 'status', 'passingYear', 'yearOfExp', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('user__username', 'job__title')
    readonly_fields = ('applied_at',)
    ordering = ('-applied_at',)


@admin.register(models.ShortlistedCandidate)
class ShortlistedCandidateAdmin(admin.ModelAdmin):
    list_display = ('id', 'job', 'candidate', 'shortlisted_at', 'notification_sent')
    list_filter = ('shortlisted_at', 'notification_sent')
    search_fields = ('job__title', 'candidate__user__username')
    readonly_fields = ('shortlisted_at',)
    ordering = ('-shortlisted_at',)
