from django.contrib import admin
from .models import CustomerState, CustomerType, Customer


class CustomerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name',)

admin.site.register(CustomerType, CustomerTypeAdmin)

class CustomerStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description',)
    search_fields = ('name',)

admin.site.register(CustomerState, CustomerStateAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'company_name', 'customer_type', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'company_name', 'contact_person_name', 'contact_person_phone', 'contact_person_email', 'email', 'other_email')
    list_filter = ('customer_type', 'status', 'country')
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Customer, CustomerAdmin)

