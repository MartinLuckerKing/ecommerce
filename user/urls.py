from django.urls import path

from user import views

app_name = 'user'


urlpatterns = [
    path('sign_up', views.sign_up, name="sign_up"),

]