from django.contrib import admin
from .models import GlobalSettings

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_under_maintenance', 'created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Novo registro
            obj.created_by = request.user
        obj.updated_by = request.user  # Atualização
        super().save_model(request, obj, form, change)
