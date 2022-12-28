from .forms import RegistrationForm
from django.contrib.auth import login
from django.shortcuts import render

# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("Inscription réussie !")
    else:
        form = RegistrationForm()
    return render(request, "registration/sign_up.html", {"form": form})
