from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
        Permitir apenas que o dono do elemento possa acessa-lo 

    """

    def has_permission(self, request, view):
        request_uid = request.parser_context["kwargs"]["uid"]
        user_uid = str(request.user.uid)

        return request_uid == user_uid
