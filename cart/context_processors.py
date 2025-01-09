# cart/context_processors.py
from .mixins import CartMixin

def cart_context(request):
    mixin = CartMixin()
    cart = mixin.get_or_create_cart(request)
    total_items = sum(item.quantity for item in cart.items.all())
    total_cost = cart.get_total_cost()
    return {
        'cart': cart,
        'total_items': total_items,
        'total_cost': total_cost
    }
