from django.urls import path
from . import views

urlpatterns = [
    path("candidate-dashboard/", views.candidate_dashboard, name='candidate_dashboard'),
    path("profile/", views.candidate_profile, name='candidate_profile'),
    path("profile/delete/", views.delete_profile, name='delete_profile'),
    path("job/<int:pk>/", views.job_detail, name='job_detail'),
    path("shortlisted/", views.shortlisted_jobs, name='shortlisted_jobs'),
    path("applied-jobs/", views.applied_jobs, name='applied_jobs'),
    path("hr-profile/<int:user_id>/", views.view_hr_profile, name='view_hr_profile'),
]
