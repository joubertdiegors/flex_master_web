from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from customers.models import Customer

class UserBasicRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'José Maria'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'placeholder': 'da Silva'}))
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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and (password != password2):
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
    phone = forms.CharField(required=True)
    postal_code = forms.CharField(required=True)
    city = forms.CharField(required=True)
    address = forms.CharField(required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Customer
        fields = ['phone', 'postal_code', 'city', 'address', 'image']
