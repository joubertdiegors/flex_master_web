from django.contrib import admin
from .models import SupplierState, SupplierType, Supplier


class SupplierTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name',)

admin.site.register(SupplierType, SupplierTypeAdmin)

class SupplierStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name',)

admin.site.register(SupplierState, SupplierStateAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier_type', 'national_number', 'tva_number', 'country', 'postal_code', 'city', 'status',)
    search_fields = ('name',)

admin.site.register(Supplier, SupplierAdmin)
