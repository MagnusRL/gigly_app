#from . import views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('discover/', views.discover, name='discover'),
    path('profile/', views.profile, name='profile'),

    path("signup/", views.signup_view, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="core_app/login.html"), name="login"),
    path("dashboard/createtask/", views.create_task, name="createtask"),
]