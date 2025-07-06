import uuid
from django.db import models
from django.contrib.auth.models import User
from branches.models import Branch
from customers.models import Customer
from products.models import Product
from payment_methods.models import PaymentMethod
from django.utils import timezone

class CashRegister(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    terminal_number = models.CharField(max_length=10)
    operator = models.ForeignKey(User, on_delete=models.PROTECT)
    opened_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)

    opening_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closing_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_machine = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-opened_at']

    def __str__(self):
        return f"Caixa {self.terminal_number} - {self.operator} ({self.opened_at.date()})"

class CashRegisterPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class FavoriteProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=20, default="#ffffff")
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Produto Favorito"
        verbose_name_plural = "Produtos Favoritos"

    def __str__(self):
        return f"{self.product.name} (Ordem: {self.order})"

class PdvSale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.PROTECT, related_name="sales")
    ticket_number = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    operator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="pdv_sales",
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_discount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    change_given = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Venda #{self.ticket_number} - {self.total_amount}€"
    
class PdvSaleItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(PdvSale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
class PdvSalePayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(PdvSale, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.payment_method.name}: {self.amount}"

class PdvHoldSale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identifier = models.CharField(max_length=50, help_text="Número ou apelido da espera (ex: João, Fila 1)")
    cash_register = models.ForeignKey(CashRegister, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True, help_text="Observação geral da espera")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Espera {self.identifier} - {self.created_at.strftime('%d/%m %H:%M')}"
    
class PdvHoldSaleItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hold_sale = models.ForeignKey(PdvHoldSale, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
