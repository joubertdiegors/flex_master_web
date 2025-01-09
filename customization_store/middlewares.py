import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from .models import GlobalSettings


class MaintenanceMiddleware:
    """
    Middleware para ativar o modo de manutenção com base na configuração de GlobalSettings.
    Permite acesso apenas a administradores autenticados, rotas específicas e arquivos estáticos/mídia.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verifica o estado do site (manutenção)
        try:
            settings_obj = GlobalSettings.objects.first()
            if settings_obj and settings_obj.site_under_maintenance:
                # Permitir acesso a arquivos estáticos e de mídia
                if self._is_static_or_media(request.path):
                    return self.get_response(request)

                # Permitir acesso às rotas específicas
                if self._is_allowed_path(request):
                    return self.get_response(request)

                # Redirecionar usuários não autenticados e não staff para a página de manutenção
                if not request.user.is_authenticated or not request.user.is_staff:
                    return HttpResponseRedirect(reverse('maintenance'))
        except GlobalSettings.DoesNotExist:
            pass

        return self.get_response(request)

    @staticmethod
    def _is_static_or_media(path):
        """Verifica se o caminho é de arquivos estáticos ou de mídia."""
        allowed_static_patterns = [
            r'^/static/',  # Arquivos estáticos
            r'^/media/',   # Arquivos de mídia
        ]
        return any(re.match(pattern, path) for pattern in allowed_static_patterns)

    @staticmethod
    def _is_allowed_path(request):
        """Verifica se a rota está na lista de exceções permitidas durante a manutenção."""
        allowed_paths = [
            reverse('maintenance'),  # Página de manutenção
            '/gestao',              # Página de login para administradores
        ]
        return request.path in allowed_paths
