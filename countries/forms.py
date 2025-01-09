from django import forms
from .models import Country

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
            'name',
            'code',
            'is_shipping_available',
            'image',
            'show_in_carousel',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'is_shipping_available': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'id_is_shipping_available'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'show_in_carousel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
        }

        labels = {
            'name': 'Nome',
            'code': 'Abreviação',
            'is_shipping_available': 'Entrega disponível?',
            'image': 'bandeira',
            'show_in_carousel': 'Mostra na Home',
        }
