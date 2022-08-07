from django.db import models


class Quote(models.Model):
    """
    Cotações

    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
