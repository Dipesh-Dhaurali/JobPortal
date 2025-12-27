from django.urls import path
from .import views

urlpatterns = [
    path("candidate-register/", views.register_candidate ,name='register_candidate'),
    path("hr-register/", views.register_hr ,name='register_hr'),
    path("login/", views.login_user ,name='login_user'),
    path("logout/", views.logoutuser ,name='logout_user'),
]
