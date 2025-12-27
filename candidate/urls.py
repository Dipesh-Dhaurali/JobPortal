from django.urls import path
from . import views

urlpatterns = [
    path("candidate-dashboard/", views.candidate_dashboard, name='candidate_dashboard'),
    path("job/<int:pk>/", views.job_detail, name='job_detail'),
    path("shortlisted/", views.shortlisted_jobs, name='shortlisted_jobs'),
]
