import admin_thumbnails
from .models import Category, Product, MultiProductImage
from django.contrib import admin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_field = {'slug': ('name',)}


@admin_thumbnails.thumbnail('images')
class MultiProductImageAdmin(admin.StackedInline):
    model = MultiProductImage


@admin.register(Product)
@admin_thumbnails.thumbnail('main_image')
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'created', 'updated']
    inlines = [MultiProductImageAdmin]
    list_filter = ['created', 'updated']
    list_editable = ['price']
    prepopulated_field = {'slug': ('name',)}

    class Meta:
        model = Product

