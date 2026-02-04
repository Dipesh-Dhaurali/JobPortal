from django.urls import path
from . import views

urlpatterns = [
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    
    # User Management
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/<int:user_id>/suspend/', views.suspend_user, name='suspend_user'),
    path('admin/users/<int:user_id>/activate/', views.activate_user, name='activate_user'),
    
    # Job Moderation
    path('admin/jobs/', views.moderate_jobs, name='moderate_jobs'),
    path('admin/jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('admin/jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    
    # Profile Viewing
    path('admin/hr-profile/<int:user_id>/', views.view_hr_profile, name='view_hr_profile'),
    path('admin/candidate-profile/<int:user_id>/', views.view_candidate_profile, name='view_candidate_profile'),
]
