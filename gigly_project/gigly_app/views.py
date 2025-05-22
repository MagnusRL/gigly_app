# Create your views here.
from django.shortcuts import render, HttpResponse

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def discover(request):
    return render(request, 'discover.html')

def profile(request):
    return render(request, 'profile.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')