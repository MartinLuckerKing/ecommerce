from shop.models import Category


def dropdown_menu(request):
    categories = Category.objects.all()
    return {'categories': categories}