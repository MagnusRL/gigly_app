from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import Task


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(label="Display Name", max_length=255)
    age = forms.IntegerField(label="Age", min_value=0)

    class Meta:
        model = User
        fields = ("email", "name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove username field if present
        self.fields.pop("username", None)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data["name"]
        user.age = self.cleaned_data["age"]
        if user.age < 18:
            user.is_seller = True
        else:
            user.is_buyer = True
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'location', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
