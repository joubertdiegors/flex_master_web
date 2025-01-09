from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Categoria'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Categoria',
            'parent': 'Categoria Pai',
            'image': 'Imagem da Categoria',
        }

        def clean_parent(self):
            parent = self.cleaned_data['parent']
            if parent and parent == self.instance:
                raise forms.ValidationError("A categoria não pode ser pai dela mesma.")
            return parent
