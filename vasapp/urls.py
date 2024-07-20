from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name=""),
    path("login/", views.login, name="login"),
    path("register/", views.registerUser, name="register"),
    path("authenticate/", views.authenticate, name="authenticate"),
    path("dashboard/", views.dashboard, name="dashboard"),

]