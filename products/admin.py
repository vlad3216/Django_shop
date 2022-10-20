from django.contrib import admin

from shop1.mixins.admin_mix import ImageMixins
from products.models import Product, Category


@admin.register(Product)
class ProductAdmin(ImageMixins, admin.ModelAdmin):
    filter_horizontal = ('products',)
    list_display = ('name', 'price', 'sku', 'created_at',)
    list_filter = ('price', 'category',)
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(ImageMixins, admin.ModelAdmin):
    list_display = ('name', 'created_at')