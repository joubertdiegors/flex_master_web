from django.db import models
from django.conf import settings
from products.models import Product
from suppliers.models import Supplier
from datetime import datetime


class SupplierProductPrice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='supplier_product_prices')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_supplier_prices')
    box_quantity = models.PositiveIntegerField(null=True, blank=True)  # Quantidade na caixa fechada
    allows_retail = models.BooleanField(default=True)  # Permite quantidade varejo (sem caixa fechada)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Valor de compra
    supplier_article_code = models.CharField(max_length=50, null=True, blank=True)  # Código do artigo no fornecedor
    last_purchase_date = models.DateField(null=True, blank=True)  # Data da última compra
    last_purchase_quantity = models.PositiveIntegerField(null=True, blank=True)  # Qtd da última compra
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_product_price_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='supplier_product_price_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('supplier', 'product')
        ordering = ['product']

    def __str__(self):
        return f"{self.product.name} - {self.supplier.name}"


class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    order_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('PENDING', 'Pendente'), ('CONFIRMED', 'Confirmado'), ('CANCELLED', 'Cancelado')], default='PENDING')
    general_notes = models.TextField(null=True, blank=True)
    receiving_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_order_created_user', on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='purchase_order_updated_user', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['order_date']

    def __str__(self):
        return f"Pedido de {self.supplier.name} em {self.order_date.strftime('%Y-%m-%d')}"
    
    def generate_order_number(self):
        now = datetime.now()
        year = str(now.year)[-2:]
        month = f'{now.month:02}'
        prefix = 'C'

        last_order = PurchaseOrder.objects.filter(order_number__startswith=f'{prefix}{year}{month}').order_by('order_number').last()

        if last_order:
            last_number = int(last_order.order_number[-4:])
            new_number =  last_number + 1
        else:
            new_number = 1
        
        return f'{prefix}{year}{month}{new_number:04}'


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Imposto aplicado ao item
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Desconto aplicado ao item
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    received_quantity = models.PositiveIntegerField(null=True, blank=True)  # Quantidade recebida
    lot_number = models.CharField(max_length=100, null=True, blank=True)  # Número do lote
    manufacture_date = models.DateField(null=True, blank=True)  # Data de fabricação do produto
    expiration_date = models.DateField(null=True, blank=True)  # Data de vencimento do produto
    notes = models.TextField(null=True, blank=True)  # Observações/Informações

    class Meta:
        unique_together = ('purchase_order', 'product')

    def calculate_total_price(self):
        # Garante que quantity e price_at_order têm valores válidos
        quantity = self.quantity or 0
        price_at_order = self.price_at_order or 0
        total = quantity * price_at_order

        if self.discount:
            total -= self.discount
        if self.tax:
            total += self.tax

        return total

    def save(self, *args, **kwargs):
        # Atualiza o preço total antes de salvar
        self.total_price = self.calculate_total_price()

        # Salva o novo preço no SupplierProductPrice se necessário
        if self.price_at_order is not None:
            supplier_product_price, created = SupplierProductPrice.objects.get_or_create(
                supplier=self.purchase_order.supplier,
                product=self.product,
                defaults={
                    'purchase_price': self.price_at_order,
                    'box_quantity': 0,  # Pode ser ajustado conforme necessário
                    'allows_retail': True,  # Pode ser ajustado conforme necessário
                    'supplier_article_code': '',  # Pode ser ajustado conforme necessário
                    'created_by': self.purchase_order.created_by,
                    'updated_by': self.purchase_order.updated_by,
                }
            )
            if not created and supplier_product_price.purchase_price != self.price_at_order:
                # Atualiza o preço se já existir e for diferente
                supplier_product_price.purchase_price = self.price_at_order
                supplier_product_price.updated_by = self.purchase_order.updated_by
                supplier_product_price.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
