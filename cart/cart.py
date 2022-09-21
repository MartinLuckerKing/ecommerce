from django.conf import settings
from shop.models import Product
from decimal import Decimal, ConversionSyntax


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        print("Initialisation de la session...")
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            print("Création du panier...")
            cart = self.session[settings.CART_SESSION_ID] = {}
            print("Panier créé !")
        self.cart = cart

    def add(self, product, quantity=1, overrride_quantity=False):
        product_id = str(product.id)
        print("Ajout au panier...")
        if product_id not in self.cart:
            print("Produit n'est pas dans le panier: Ajout au panier en cours...")
            self.cart[product_id] = {'quantity': 0, 'price': product.price}
            print("Ajout réussi !")

        if overrride_quantity:
            print("Produit est déjà dans le panier")
            self.cart[product_id]['quantity'] = quantity
            print("Ajout réussi !")
        else:
            self.cart[product_id]['quantity'] += quantity
            print("Ajout réussi !")
        self.save()

    def save(self):
        self.session.modified = True
        print("Modification sauvegardé...")

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            print("Produit supprimé...")
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

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()