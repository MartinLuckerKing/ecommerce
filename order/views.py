import decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import json
from cart.cart import Cart
from cart.forms import CartAddProductForm
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from shop.models import Product


@login_required(login_url='login')
def checkout(request):
    cart = Cart(request)
    form = OrderForm(request.POST)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'override': True})
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'order/checkout.html', context)


def payment(request):
    cart = Cart(request)
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    total_price = cart.get_total_price()
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = total_price,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = cart

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.get('product_id')
        orderproduct.quantity = item.get('quantity')
        orderproduct.product_price = item.get('price')
        orderproduct.total_price_per_product = cart.get_total_price_by_item(product=item)
        orderproduct.total_price = cart.get_total_price()
        orderproduct.ordered = True
        orderproduct.save()

        quantity = item.get('quantity')
        stock = item.get('product').stock
        print(stock)
        product = Product.objects.get(id=item.get('product_id'))
        new_stock = stock - quantity
        product.stock = new_stock
        product.save(update_fields=['stock'])
        print(new_stock)
    return render(request, 'order/order_complete.html')


def place_order(request, total=0):
    tax = decimal.Decimal(0.2)
    current_user = request.user
    cart = Cart(request)
    cart_total = cart.get_total_price()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = cart_total
            data.tax = cart_total*tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                #'cart_items': cart_items,
                'total': total,
                'form': form,
                'cart': cart,
                #'tax': tax,
                #'grand_total': grand_total,
            }
            return render(request, 'order/payment.html', context)
    else:
        return redirect('checkout')


def order_complete(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'order/order_complete.html')


