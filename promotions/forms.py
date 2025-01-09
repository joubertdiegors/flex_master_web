from django import forms
from .models import Promotion
from .fields import CustomDecimalField
from products.models import Product

class PromotionForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Produto'
    )
    promotion_price = CustomDecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Preço da Promoção'
    )

    class Meta:
        model = Promotion
        fields = [
            'product',
            'promotion_price',
            'description',
            'start_date',
            'end_date',
            'active',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'})
        }
        labels = {
            'description': 'Descrição',
            'start_date': 'Data de Início',
            'end_date': 'Data de Término',
            'active': 'Ativo',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - {obj.brand if obj.brand else ''} {obj.volume if obj.volume else ''} {obj.package_unit.symbol if obj.package_unit else ''}"
