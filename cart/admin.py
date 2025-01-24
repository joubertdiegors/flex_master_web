from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0  # Não exibe linhas extras
    readonly_fields = ('product', 'quantity', 'price', 'promotion', 'get_cost')
    fields = ('product', 'quantity', 'price', 'promotion', 'get_cost')  # Ordem dos campos
    can_delete = False  # Impede a exclusão diretamente no inline

    def get_cost(self, obj):
        return f"€{obj.get_cost():.2f}"
    get_cost.short_description = "Custo Total"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'created_at', 'updated_at', 'get_total_cost')
    list_filter = ('created_at', 'updated_at')  # Filtros laterais
    search_fields = ('user__username', 'session_key')  # Campos para busca
    readonly_fields = ('created_at', 'updated_at', 'get_total_cost')
    inlines = [CartItemInline]  # Relacionamento inline

    def get_total_cost(self, obj):
        return f"€{obj.get_total_cost():.2f}"
    get_total_cost.short_description = "Custo Total do Carrinho"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'price', 'promotion', 'get_cost')
    list_filter = ('cart', 'promotion')  # Filtros laterais
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('get_cost',)

    def get_cost(self, obj):
        return f"€{obj.get_cost():.2f}"
    get_cost.short_description = "Custo Total"
