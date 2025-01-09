from django.contrib import admin
from . import models

class SupplierProductPriceAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product', 'purchase_price', 'box_quantity', 'created_at', 'updated_at')
    list_filter = ('supplier', 'product', 'created_at')
    search_fields = ('supplier__name', 'product__name', 'supplier_article_code')

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'order_date', 'status', 'expected_delivery_date', 'created_at', 'updated_at')
    list_filter = ('supplier', 'status', 'order_date')
    search_fields = ('supplier__name',)

class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'product', 'quantity', 'price_at_order', 'total_price', 'received_quantity')
    list_filter = ('purchase_order__supplier', 'product')
    search_fields = ('product__name', 'purchase_order__supplier__name')

admin.site.register(models.SupplierProductPrice, SupplierProductPriceAdmin)
admin.site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(models.PurchaseOrderItem, PurchaseOrderItemAdmin)
