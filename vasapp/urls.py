from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.home, name=""),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerUser, name="register"),
    # path("authenticate/", views.authenticate, name="authenticate"),
    path("dashboard/", views.dashboard, name="dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)