# cart/mixins.py
from .models import Cart

class CartMixin:
    def get_cart(self, request):
        if request.user.is_authenticated:
            return Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if not session_key:
                return None
            return Cart.objects.filter(session_key=session_key).first()

    def create_cart(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

# class CartMixin:
#     def get_or_create_cart(self, request):
#         if request.user.is_authenticated:
#             cart, created = Cart.objects.get_or_create(user=request.user)
#         else:
#             session_key = request.session.session_key
#             if not session_key:
#                 request.session.create()
#                 session_key = request.session.session_key
#             cart, created = Cart.objects.get_or_create(session_key=session_key)
#         return cart