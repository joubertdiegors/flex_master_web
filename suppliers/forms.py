from django import forms
from . import models

class SupplierTypeForm(forms.ModelForm):
    class Meta:
        model = models.SupplierType
        fields = [
            'name',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }

class SupplierStateForm(forms.ModelForm):
    class Meta:
        model = models.SupplierState
        fields = [
            'name',
            'description',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = models.Supplier
        fields = [
            'name',
            'supplier_type',
            'national_number',
            'tva_number',
            'phone',
            'email',
            'country',
            'postal_code',
            'city',
            'address',
            'comments',
            'image',
            'status',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier_type': forms.Select(attrs={'class': 'form-control'}),
            'national_number': forms.TextInput(attrs={'class': 'form-control'}),
            'tva_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome',
            'customer_type': 'Tipo de Cliente',
            'national_number': 'Número Nacional',
            'tva_number': 'Número de TVA',
            'phone': 'Telefone',
            'email': 'E-mail',
            'country': 'País',
            'postal_code': 'Código Postal',
            'city': 'Cidade',
            'address': 'Endereço',
            'comments': 'Comentários',
            'image': 'Imagem',
            'status': 'Estado',
        }
