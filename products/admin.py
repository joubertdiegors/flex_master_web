from django.contrib import admin
from .models import SalesUnit, PackageUnit, Brand, Product, Ingredients, NutritionalItem, NutritionalInfo
from categories.models import Category
from django import forms


class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)

admin.site.register(Brand, BrandAdmin)

class SalesUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol', 'is_fractional',)
    search_fields = ('name',)

admin.site.register(SalesUnit, SalesUnitAdmin)

class PackageUnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'symbol',)
    search_fields = ('name',)

admin.site.register(PackageUnit, PackageUnitAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'barcode',
        'name',
        'volume',
        'package_unit',
        'brand',
        'country',
        'get_categories',  # Use 'get_categories' here
        'sales_unit',
        'net_weight',
        'gross_weight',
        'stock_control',
        'minimum_stock',
        'maximum_stock',
        'selling_price',
        'is_active',
        'created_at',
        'updated_at',
        'created_by',
        'updated_by',
    )
    search_fields = ('name', 'barcode', 'brand', 'category__name')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories'

admin.site.register(Product, ProductAdmin)

class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('product', 'ingredients', 'allergens', 'conservation_instructions')
    search_fields = ('product__name', 'ingredients', 'allergens')
    list_filter = ('product',)

admin.site.register(Ingredients, IngredientsAdmin)

class NutritionalItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'package_unit')
    search_fields = ('name',)
    list_filter = ('package_unit',)

admin.site.register(NutritionalItem, NutritionalItemAdmin)

class NutritionalInfoInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'nutritional_item', 'quantity')
    search_fields = ('product__name', 'nutritional_item__name')
    list_filter = ('product', 'nutritional_item')
    raw_id_fields = ('product', 'nutritional_item')

admin.site.register(NutritionalInfo, NutritionalInfoInfoAdmin)
