from django import forms

class CheckboxSelectMultipleWithHeight(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        self.height = kwargs.pop('height', '200px')  # Default height
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        return f'<div style="height: {self.height}; overflow-y: auto;">{html}</div>'
