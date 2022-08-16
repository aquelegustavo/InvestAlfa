from django.apps import AppConfig


class QuotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investalfa.apps.quotes'

    def ready(self):
        from .scheduler import start
        start()
