from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'created_at', 'updated_at', 'created_by', 'updated_by')
    search_fields = ('name',)

admin.site.register(models.Category, CategoryAdmin)
