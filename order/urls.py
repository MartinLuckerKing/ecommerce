from django.urls import path
from order import views


app_name = 'order'

urlpatterns = [
    path('checkout', views.checkout, name="checkout"),
    path('payment', views.payment, name="payment"),
    path('order_complete', views.order_complete, name="order_complete"),
    path('place_order/', views.place_order, name="place_order"),


    ]