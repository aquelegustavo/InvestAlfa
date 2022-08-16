""" 
Modelo do banco de dados

"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password


class CustomUser(AbstractUser):
    """
    Classe CustomUser

    Modificação da classe padrão de usuários

    Attributes:
        uid: Id do usuário
        email: Email do usuário
        password: Senha do usuário

    """

    uid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=32, validators=[validate_password])
