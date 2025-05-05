from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile

# Formulário simples para criação de usuários
class UserCreationSimpleForm(forms.ModelForm):
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmação de senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Inline para edição posterior
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Admin personalizado
class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationSimpleForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    inlines = [UserProfileInline]

# Registrar
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
