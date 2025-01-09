# cart/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from promotions.models import Promotion

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_user', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username if self.user else 'Anonymous'}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.ForeignKey(Promotion, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        # Verificar se o produto está em promoção e ajustar o preço
        if self.promotion:
            self.price = self.promotion.promotion_price
        else:
            self.price = self.product.selling_price

        super().save(*args, **kwargs)
