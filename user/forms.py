from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "age"]