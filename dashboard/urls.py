from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('my_orders/<int:user_id>', views.my_orders, name="my_orders"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('change_password', views.change_password, name="change_password"),



    ]