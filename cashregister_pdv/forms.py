from django import forms
from .models import FavoriteProduct

COLOR_CHOICES = [
    ("#FF0000", "Vermelho"),
    ("#00A65A", "Verde"),
    ("#007BFF", "Azul"),
    ("#FFC107", "Amarelo"),
    ("#6C757D", "Cinza"),
    ("#FF69B4", "Rosa"),
    ("#8A2BE2", "Roxo"),
    ("#000000", "Preto"),
]

class FavoriteProductForm(forms.ModelForm):
    color = forms.ChoiceField(choices=COLOR_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))

    class Meta:
        model = FavoriteProduct
        fields = ['product', 'color', 'order']
