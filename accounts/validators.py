from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    """
    Personaliza a mensagem de erro quando a senha é parecida com o nome do usuário.
    """

    def validate(self, password, user=None):
        if user:
            user_attributes = [user.get_username(), user.first_name, user.last_name]
            for attribute in user_attributes:
                if attribute and attribute.lower() in password.lower():
                    raise ValidationError(
                        _("Sua senha não pode conter informações pessoais como seu nome ou sobrenome."),
                        code='password_too_similar',
                    )
