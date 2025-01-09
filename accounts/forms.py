from django import forms
from django.contrib.auth.models import User
from customers.models import Customer, Country

class UserBasicRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', widget=forms.TextInput(attrs={'placeholder': 'José Maria'}))
    last_name = forms.CharField(label='Sobrenome', widget=forms.TextInput(attrs={'placeholder': 'da Silva'}))
    email = forms.EmailField(label='e-mail', widget=forms.EmailInput(attrs={'placeholder': 'email@gmail.com'}))
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirme a senha')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

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
    class Meta:
        model = Customer
        fields = ['phone', 'postal_code', 'city', 'address', 'image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
