from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms


class RegistrationForm(UserCreationForm):

    age = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(({'placeholder': 'Nom de Compte'}))
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Prénom'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Nom de Famille'})
        self.fields['age'].widget.attrs.update({'placeholder': 'Age'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Mot de passe'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Répétez le Mot de Passe'})

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "age", "password1")

        labels = {
            'username': 'Nom de Compte',
            'email': 'Email',
            'first_name': 'Prénom',
            'last_name': 'Nom de Famille',
            'age': 'age',
            'password1': 'Mot de passe',
            'password2': 'Répétez le Mot de Passe',
        }


class EditProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ["last_name", "first_name", "email"]
        labels = {
            'email': 'Email',
            'last_name':'Nom de famille',
            'first_name': 'Prénom',
        }