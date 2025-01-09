# promotions/admin.py
from django.contrib import admin
from .models import Promotion

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'promotion_price', 'start_date', 'end_date', 'active')
    list_filter = ('active',)
    search_fields = ('product__name',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('product', 'promotion_price', 'description', 'start_date', 'end_date', 'active')
        }),
    )
admin.site.register(Promotion, PromotionAdmin)