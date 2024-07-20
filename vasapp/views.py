from django.shortcuts import render


def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def registerUser(request):
    return render(request, "register.html")

def authenticate(request):
    pass

def dashboard(request):
    pass