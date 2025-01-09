from django.contrib import admin
from . import models

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_shipping_available', 'created_at', 'updated_at')
    list_filter = ('is_shipping_available', 'created_at')
    search_fields = ('name', 'code')

admin.site.register(models.Country, CountryAdmin)
