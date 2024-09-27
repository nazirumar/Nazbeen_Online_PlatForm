from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm




class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]