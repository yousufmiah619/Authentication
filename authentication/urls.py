from django.urls import path
from .views import *
urlpatterns = [
    path("register/",Register.as_view()),
    path("login/",Login.as_view()),
    path("profile/",Profile.as_view()),
    path("changepassword/",ChangePassword.as_view())
]