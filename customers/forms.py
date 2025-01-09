from django import forms
from . import models

class CustomerTypeForm(forms.ModelForm):
    class Meta:
        model = models.CustomerType
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

class CustomerStateForm(forms.ModelForm):
    class Meta:
        model = models.CustomerState
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

class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = [
            'user',
            'customer_type',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birth_date',
            'company_name',
            'tva_number',
            'contact_person_name',
            'contact_person_phone',
            'contact_person_email',
            'other_email',
            'country',
            'postal_code',
            'city',
            'address',
            'comments',
            'image',
            'status',
        ]
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'customer_type': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'tva_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'other_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'Usuário',
            'customer_type': 'Tipo de Cliente',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'Email',
            'phone': 'Telefone',
            'birth_date': 'Data de Nascimento',
            'company_name': 'Nome da Empresa',
            'tva_number': 'Número de TVA',
            'contact_person_name': 'Nome da Pessoa de Contato',
            'contact_person_phone': 'Telefone da Pessoa de Contato',
            'contact_person_email': 'Email da Pessoa de Contato',
            'other_email': 'Outro Email',
            'country': 'País',
            'postal_code': 'Código Postal',
            'city': 'Cidade',
            'address': 'Endereço',
            'comments': 'Comentários',
            'image': 'Imagem',
            'status': 'Estado',
        }

