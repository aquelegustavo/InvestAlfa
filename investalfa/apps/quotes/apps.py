"""
Configuração da aplicação

"""
from django.apps import AppConfig


class QuotesConfig(AppConfig):
    """
    Classe de configuração da aplicação

    Attributes:
        default_auto_field: Campo padrão do modelo
        name: Nome da aplicação

    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investalfa.apps.quotes'

    def ready(self):
        """
        Função chamada quando aplicação carregou

        Inicia agendamento de tarefas
        """
        from .scheduler import start
        start()
