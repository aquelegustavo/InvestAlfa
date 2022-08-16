"""
Configuração da aplicação

"""

from django.apps import AppConfig


class CompaniesConfig(AppConfig):
    """
    Classe de configuração da aplicação

    Attributes:
        default_auto_field: Campo padrão do modelo
        name: Nome da aplicação

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investalfa.apps.companies'
