"""
Permissões relacionadas ao usuário

"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Classe de permissão 

    Permitir apenas que o dono do elemento possa acessa-lo 

    """

    def has_permission(self, request, view):
        """
        Tem permissão

        Arguments:
            request: instância de requisição
            view: instância da view

        Return: (bool) usuário está autorizado ou não
        """
        request_uid = request.parser_context["kwargs"]["uid"]
        user_uid = str(request.user.uid)

        return request_uid == user_uid
