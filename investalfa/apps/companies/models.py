""" 
Modelo do banco de dados

"""
from django.db import models


class Company(models.Model):
    """
    Classe Empresa

    Attributes:
        code: Código da bolsa da empresa
        name: Nome da empresa
        last_quote: Última cotação da empresa
        min_quote: Menor cotação registrada
        max_quote: Maior cotação registrada

        """
    code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=100)
    last_quote = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True, default=None)
    min_quote = models.DecimalField(
        max_digits=6, decimal_places=2)
    max_quote = models.DecimalField(
        max_digits=6, decimal_places=2)
