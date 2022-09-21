from django.contrib import admin
from .models import Category, Product, MultiProductImage
from order.models import Order
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_field = {'slug': ('name',)}


class MultiProductImageAdmin(admin.StackedInline):
    model = MultiProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image', 'price', 'available', 'created', 'updated']
    inlines = [MultiProductImageAdmin]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_field = {'slug': ('name',)}

    class Meta:
       model = Product


@admin.register(MultiProductImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class Order(admin.ModelAdmin):
    pass