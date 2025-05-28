from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TaskForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.http import HttpResponseForbidden


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    tasks = Task.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {
        "user": request.user,
        "tasks": tasks,
    })

def discover(request):
    return render(request, 'discover.html')

def profile(request):
    return render(request, 'profile.html')

def login_page(request):
    return render(request, 'login.html')

def signup_page(request):
    return render(request, 'signup.html')

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            age = form.cleaned_data.get('age')
            user.age = age

            if age < 18:
                user.is_buyer = True
            else:
                user.is_seller = True

            user.save()
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("dashboard")
    else:
        form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})

@login_required
def create_task(request):
    if not request.user.is_buyer:
        return HttpResponseForbidden("Only buyers can create tasks.")

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.buyer = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'createtask.html', {'form': form})
