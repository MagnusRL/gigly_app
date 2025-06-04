from django.urls import path
from . import views # Or from your_app import views if the views are in a different file

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('chat/<str:group_name>/', views.chat_view, name='chat'),
    path('create-group/', views.create_group, name='create_group'),
]
