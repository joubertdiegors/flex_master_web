from django import forms
from django.forms.models import inlineformset_factory
from .models import SupplierProductPrice, PurchaseOrder, PurchaseOrderItem
from products.models import Product
from django.utils import timezone

class SupplierProductPriceForm(forms.ModelForm):
    class Meta:
        model = SupplierProductPrice
        fields = [
            'supplier', 'product', 'box_quantity', 'allows_retail',
            'purchase_price', 'supplier_article_code', 'last_purchase_date',
            'last_purchase_quantity'
        ]
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control SupplierProductPriceForm supplier-select'}),
            'product': forms.Select(attrs={'class': 'form-control SupplierProductPriceForm product-select'}),
            'box_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'allows_retail': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'supplier_article_code': forms.TextInput(attrs={'class': 'form-control'}),
            'last_purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'last_purchase_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['order_number', 'supplier', 'order_date', 'expected_delivery_date', 'status', 'general_notes', 'receiving_notes']

class PurchaseOrderItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrderItem
        fields = ['product', 'quantity', 'price_at_order', 'tax', 'discount', 'total_price', 'received_quantity', 'lot_number', 'manufacture_date', 'expiration_date', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control js-example-tags product-select', 'style': 'width: 100%;'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
            'price_at_order': forms.NumberInput(attrs={'class': 'form-control price-input', 'style': 'width: 100px;', 'readonly': 'readonly'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
            'total_price': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100px;'}),
        }

PurchaseOrderItemFormSet = inlineformset_factory(
    PurchaseOrder,
    PurchaseOrderItem,
    form=PurchaseOrderItemForm,
    extra=0,
    can_delete=True
)
