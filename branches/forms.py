from django import forms
from . import models

class BranchForm(forms.ModelForm):
    class Meta:
        model = models.Branch
        fields = [
            'name',
            'tva',
            'unit_etablissement',
            'open_date',
            'phone',
            'email',
            'site',
            'country',
            'postal_code',
            'street',
            'number',
            'complement',
            'neighborhood',
            'city',
            'state',
            'image',
            'description',
            'is_active',
            'close_date',
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'tva': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_etablissement': forms.TextInput(attrs={'class': 'form-control'}),
            'open_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'site': forms.URLInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'complement': forms.TextInput(attrs={'class': 'form-control'}),
            'neighborhood': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'id_is_active_branche'}),
            'close_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

        labels = {
            'name': 'Nome',
            'tva': 'TVA',
            'unit_etablissement': 'N. Estabelecimento',
            'open_date': 'Data de Abertura',
            'phone': 'Telefone',
            'email': 'E-mail',
            'site': 'Site',
            'country': 'País',
            'postal_code': 'Código Postal',
            'street': 'Rua',
            'number': 'Número',
            'complement': 'Complemento',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'image': 'Logo',
            'description': 'Descrição',
            'is_active': 'Loja ativa?',
            'close_date': 'Data de Encerramento',
        }
