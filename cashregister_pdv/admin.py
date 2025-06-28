from django.contrib import admin
from .models import FavoriteProduct

@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'color', 'created_by')
    list_select_related = ('product',)
    ordering = ['order']
    search_fields = ['product__name']
