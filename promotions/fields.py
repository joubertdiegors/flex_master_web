from django import forms

class CustomDecimalField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.replace(',', '.')
        return super().to_python(value)