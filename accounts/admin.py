from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Perfil do Usuário"

# Estende o admin padrão do User
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
    list_display = ("username", "email", "first_name", "last_name", "is_staff")

# Remove o admin padrão e registra o novo
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
