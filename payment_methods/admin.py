from django.contrib import admin
from .models import PaymentMethod

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "show_on_pdv", "order")
    ordering = ["order"]

admin.site.register(PaymentMethod, PaymentMethodAdmin)
