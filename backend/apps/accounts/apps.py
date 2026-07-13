# ===========================================
# FILMERSHUB - CONFIGURAÇÃO DA APP ACCOUNTS
# ===========================================

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuração da app de contas de usuário."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Contas de Usuário'

    def ready(self):
        """Executa quando a app é carregada."""
        # Importa signals (se houver)
        # import apps.accounts.signals  # noqa
