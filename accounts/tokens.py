from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Gera e valida tokens de verificação de e-mail para o Customer.
    O método _make_hash_value inclui o campo is_email_verified
    para invalidar o token caso o e-mail já tenha sido verificado.
    """
    def _make_hash_value(self, customer, timestamp):
        return f"{customer.pk}{timestamp}{customer.is_email_verified}"

email_verification_token = EmailVerificationTokenGenerator()