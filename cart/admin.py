from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'promotion', 'get_cost')
    fields = ('product', 'quantity', 'price', 'promotion', 'get_cost')
    can_delete = False

    def get_cost(self, obj):
        if obj.price is None or obj.quantity is None:
            return "€0.00"
        return f"€{obj.get_cost():.2f}"
    get_cost.short_description = "Custo Total"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'session_key', 'created_at', 'updated_at', 'get_total_cost', 'view_items_link')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('created_at', 'updated_at', 'get_total_cost')
    inlines = [CartItemInline]

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        return "Anônimo"
    user_display.short_description = "Usuário"

    def get_total_cost(self, obj):
        return f"€{obj.get_total_cost():.2f}"
    get_total_cost.short_description = "Custo Total do Carrinho"

    def view_items_link(self, obj):
        return format_html(
            '<a href="/admin/cart/cartitem/?cart__id__exact={}">Ver Itens</a>', obj.id
        )
    view_items_link.short_description = "Itens no Carrinho"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'promotion', 'get_cost')
    list_filter = ('cart', 'promotion')
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('get_cost',)

    def get_cost(self, obj):
        return f"€{obj.get_cost():.2f}"
    get_cost.short_description = "Custo Total"
