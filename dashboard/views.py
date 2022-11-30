import django.contrib.messages.middleware
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import message
from django.http import HttpResponseRedirect
from django.shortcuts import render
from order.models import Order, Payment, OrderProduct
from django.contrib.auth.models import User
from user.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


# Create your views here.


@login_required(login_url='login')
def dashboard(request):

    return render(request, 'dashboard/dashboard.html')


@login_required(login_url='login')
def my_orders(request, user_id):
    if request.method == 'GET':
        order = Order.objects.all()
        user = User.objects.get(id=user_id)
        context = {
            'order': order,
            'user': user
        }
        return render(request, 'dashboard/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):

    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = EditProfileForm(request.POST, instance=request.user)
            if fm.is_valid():
                messages.success(request, 'Profile Updated')
                fm.save()
        else:
            fm = EditProfileForm(instance=request.user)
        return render(request, 'dashboard/edit_profile.html', {'name': request.user, 'form': fm})
    else:
        return render(request, 'shop/home_page.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        fm = PasswordChangeForm(user=request.user, data=request.POST)
        if fm.is_valid():
            fm.save()
            print("Password changer")
            return HttpResponseRedirect('dashboard/change_password.html')
    else:
        fm = PasswordChangeForm(user=request.user)
    return render(request, 'dashboard/change_password.html', {'form': fm})
