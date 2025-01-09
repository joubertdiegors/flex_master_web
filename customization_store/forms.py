from django import forms
from . import models
from products.models import Brand, Product

class HeaderLogoForm(forms.Form):
    header_logo = forms.ImageField(label='Logo do Header')

class NavbarLogoForm(forms.Form):
    navbar_logo = forms.ImageField(label='Logo do Navbar')

class FaviconForm(forms.Form):
    favicon = forms.ImageField(label='Favicon')

class ProductImageForm(forms.Form):
    product_default = forms.ImageField(label='Imagem padão para produtos.')

class CustomerImageForm(forms.Form):
    customer_default = forms.ImageField(label='Imagem padão para clientes.')

class SupplierImageForm(forms.Form):
    supplier_default = forms.ImageField(label='Imagem padão para fornecedores.')

class BannerForm(forms.ModelForm):
    class Meta:
        model = models.Banner
        fields = [
            'title',
            'description',
            'image',
            'link',
            'start_date',
            'end_date',
            'active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'image': 'Imagem',
            'link': 'Link',
            'start_date': 'Data de Início',
            'end_date': 'Data de Fim',
            'active': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.start_date:
                self.fields['start_date'].initial = self.instance.start_date.strftime('%Y-%m-%d')
            if self.instance.end_date:
                self.fields['end_date'].initial = self.instance.end_date.strftime('%Y-%m-%d')

class BestSellerProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Produto'
    )
    
    class Meta:
        model = models.BestSellerProduct
        fields = [
            'product',
            'description',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'isActiveSwitch'})
        }
        labels = {
            'description': 'Descrição',
            'is_active': 'Produto Ativo?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - {obj.brand if obj.brand else ''} {obj.volume if obj.volume else ''} {obj.package_unit.symbol if obj.package_unit else ''}"

class FreshProductsForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Produto'
    )

    class Meta:
        model = models.FreshProducts
        fields = [
            'product',
            'description',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'isActiveSwitch'})
        }
        labels = {
            'description': 'Descrição',
            'is_active': 'Produto Ativo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].label_from_instance = lambda obj: f"{obj.name} - {obj.brand if obj.brand else ''} {obj.volume if obj.volume else ''} {obj.package_unit.symbol if obj.package_unit else ''}"

class HighlightedBrandForm(forms.ModelForm):
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Marca'
    )

    class Meta:
        model = models.HighlightedBrand
        fields = [
            'brand',
            'description',
            'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch', 'id': 'isActiveSwitch'})
        }
        labels = {
            'description': 'Descrição',
            'is_active': 'Marca Ativa?'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.all()
        self.fields['brand'].label_from_instance = lambda obj: f"{obj.name}"