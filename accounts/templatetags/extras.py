from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    print("add_class filter loaded")  # Debugging statement
    return field.as_widget(attrs={"class": css_class})
