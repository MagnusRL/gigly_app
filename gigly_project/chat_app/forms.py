from django.forms import ModelForm
from django import forms
from .models import ChatMessage, ChatGroup

class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['body']
        widgets = {
        'body': forms.TextInput(attrs={
            'class': 'form-control me-2',
            'maxlength': '300',
            'autofocus': True,
            'placeholder': 'Type your message...',
            }),
        }