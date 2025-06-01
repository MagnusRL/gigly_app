from django.urls import path
from . import views # Or from your_app import views if the views are in a different file

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
]