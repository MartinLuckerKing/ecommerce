from django.shortcuts import render, get_object_or_404
from .models import Category, Product, MultiProductImage
from cart.forms import CartAddProductForm


def home_page(request):
    categories = Category.objects.all()
    chouchou = Product.objects.filter(category=1)
    noeud_papillon = Product.objects.filter(category=2)
    context = {
        'categories': categories,
        'chouchou': chouchou,
        'noeud_papillon': noeud_papillon,
               }
    return render(request, 'shop/home_page.html', context)


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products,
               }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    multiimages = MultiProductImage.objects.filter(product_id=product.id)
    cart_product_form = CartAddProductForm()
    context = {
        'cart_product_form': cart_product_form,
        'product': product,
        'multiimages': multiimages,

    }

    return render(request, 'shop/product/detail.html', context)



