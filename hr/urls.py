from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("blog/<slug:slug>/", views.blog_detail, name='blog_detail'),
    path("hrdash/", views.hrhome, name='hrdash'),
    path("postjob/", views.post_job, name='postjob'),
    path("edit-job/<int:pk>/", views.edit_job, name='edit_job'),
    path("delete-job/<int:pk>/", views.delete_job, name='delete_job'),
    path("candidate-details/<int:pk>/", views.candidate_details, name='candidate_details'),
    path("select-candidate/<int:pk>/", views.select_candidate, name='select_candidate'),
    path("reject-candidate/<int:pk>/", views.reject_candidate, name='reject_candidate'),
    path("select-final-candidate/<int:pk>/", views.select_final_candidate, name='select_final_candidate'),
    path("reject-from-shortlist/<int:pk>/", views.reject_from_shortlist, name='reject_from_shortlist'),
    path("view-candidate-profile/<int:user_id>/", views.view_candidate_profile, name='view_candidate_profile'),
]
