from django.db import models


class Quote(models.Model):
    """
    Cotação

    Attributes:
        parent_company (Company): Referência para empresa da cotação
        value: Valor da cotação (em reais)
        timestamp: Carimbo de data e hora da leitura


    """

    parent_company = models.ForeignKey(
        'companies.Company',  # Dica: use este formato para evitar erro de "importação circula"
        on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
