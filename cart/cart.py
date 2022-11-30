from django.conf import settings
from shop.models import Product
from decimal import Decimal


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, overrride_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'product_id': product.id, 'quantity': 0, 'price': product.price, 'stock': product.stock, 'product': Product()}

        if overrride_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['quantity'] * item['price']) for item in self.cart.values())

    def get_product_name(self):
        return Product.objects.create(product_name=Product.name)

    def get_quantity(self):
        return sum([item['quantity'] for item in self.cart.values()])

    def get_total_price_by_item(self, product):
        return sum([product['quantity'] * product['price']])

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
