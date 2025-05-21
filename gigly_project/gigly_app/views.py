# Create your views here.
from django.shortcuts import render, HttpResponse

def home(request):
    return render(request, 'index.html', {"active_page": "home"})

def discover(request):
    return render(request, 'discover.html', {"active_page": "discover"})

def profile(request):
    return render(request, 'profile.html', {"active_page": "profile"})