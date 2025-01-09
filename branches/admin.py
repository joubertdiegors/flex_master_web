from django.contrib import admin
from . import models

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'city')
    search_fields = ('name', 'city', 'postal_code', 'address')

admin.site.register(models.Branch, BranchAdmin)