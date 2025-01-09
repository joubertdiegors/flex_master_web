from .models import Cart, CartItem

class TransferCartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            session_key = request.session.session_key
            old_session_key = request.session.get('old_session_key')

            if old_session_key:
                try:
                    anonymous_cart = Cart.objects.get(session_key=old_session_key)
                    user_cart, created = Cart.objects.get_or_create(user=request.user)

                    for item in anonymous_cart.items.all():
                        cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                        if created:
                            cart_item.quantity = item.quantity
                        else:
                            cart_item.quantity += item.quantity
                        cart_item.price = item.price
                        cart_item.promotion = item.promotion
                        cart_item.save()

                    anonymous_cart.delete()
                except Cart.DoesNotExist:
                    pass

        return response
