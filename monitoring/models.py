from django.db import models


class Monitoring(models.Model):
    """
    Monitoramento

    Attributes:
        company (companies.Company):  Referência para empresa a ser monitorada
        user (users.CustomUser): Referência ao usuário que deseja monitorar
        frequency (int): Frequência de monitoramento.
        tunnel_min (float): Túnel - preço mínimo
        tunnel_max (float): Túnel - preço máximo
    """

    company = models.ForeignKey(
        'companies.Company',  # Dica: use este formato para evitar erro de "importação circula"
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE)

    frequency = models.PositiveSmallIntegerField()

    tunnel_min = models.DecimalField(max_digits=6, decimal_places=2)
    tunnel_max = models.DecimalField(max_digits=6, decimal_places=2)
