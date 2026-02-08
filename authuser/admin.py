from django.contrib import admin
from authuser.models import UserProfile, ContactMessage

@admin.register(UserProfile)
class UserTypeAndVerificationAdmin(admin.ModelAdmin):
    """
    Manages user type classification and verification status.
    NOTE: This is DIFFERENT from Django's Groups/Users system.
    - Groups/Users: Django's built-in role/permission system
    - UserProfile: Our custom user classification (Candidate/HR/Admin) + verification status
    """
    list_display = ('id', 'user', 'user_type', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Type & Verification', {
            'fields': ('user', 'user_type', 'phone_number', 'is_verified'),
            'description': 'Classifies user as Candidate, HR/Recruiter, or Admin. Different from Django Groups/Users.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            self.message_user(request, f"User profile created for {obj.user.username}")
    
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        """Mark selected users as verified"""
        updated_count = queryset.update(is_verified=True)
        self.message_user(request, f"Successfully verified {updated_count} user(s).")
    verify_users.short_description = "Mark selected users as verified"
    
    def unverify_users(self, request, queryset):
        """Mark selected users as unverified"""
        updated_count = queryset.update(is_verified=False)
        self.message_user(request, f"Successfully unverified {updated_count} user(s).")
    unverify_users.short_description = "Mark selected users as unverified"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Display contact form messages - Read-only access only"""
    list_display = ('id', 'name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at', 'is_read')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Message Details', {
            'fields': ('name', 'email', 'message'),
        }),
        ('Meta Information', {
            'fields': ('created_at', 'is_read'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent admin from adding messages"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Prevent admin from deleting messages"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent admin from modifying messages"""
        return False
