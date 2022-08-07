from django.db import models


class Company(models.Model):
    """
        Empresa

        Attributes:
            name: Nome da empresa
            code: Código da bolsa da empresa
            last_quote: Última cotação da empresa

        """

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    last_quote = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, default=None)
