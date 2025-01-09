from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from products.models import Product

class Promotion(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='promotion_product')
    promotion_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.promotion_price}"

    def clean(self):
        # Verifica se já existe outra promoção ativa para o mesmo produto
        if self.active and Promotion.objects.filter(product=self.product, active=True).exclude(id=self.id).exists():
            raise ValidationError("Já existe uma promoção ativa para este produto.")

    def save(self, *args, **kwargs):
        # Desativa todas as promoções anteriores do mesmo produto ao salvar uma nova promoção ativa
        if self.active:
            Promotion.objects.filter(product=self.product, active=True).exclude(id=self.id).update(active=False)
        super().save(*args, **kwargs)
