from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from customers.models import Customer
import re

class UserBasicRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'José/Maria'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'placeholder': 'Ramos/Silva'}))
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput(attrs={'placeholder': 'email@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está castrado!')
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Validações para a senha
        if len(password) < 8:
            raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("A senha deve conter pelo menos um número.")

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            self.add_error('password2', 'As senhas não conferem.')
        return cleaned_data

class CustomerBasicRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['country']
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'country': 'País',
        }

class CustomerCompleteRegistrationForm(forms.ModelForm):
    phone = forms.CharField(
        label='Telefone para contato:',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+32469124469'})
    )
    postal_code = forms.CharField(
        label='Código postal:',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '1030'})
    )
    city = forms.CharField(
        label='Cidade:',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Bruxelas'})
    )
    address = forms.CharField(
        label='Endereço com número:',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Avenue de Roodebeek, 100'})
    )
    image = forms.ImageField(
        label='Foto (opcional):',
        required=False
    )

    class Meta:
        model = Customer
        fields = ['phone', 'postal_code', 'city', 'address', 'image']
