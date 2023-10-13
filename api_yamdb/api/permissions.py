from rest_framework import permissions

from django.contrib.auth import get_user_model

User = get_user_model()


class IsAdmin(permissions.BasePermission):
    """Доступ только для админов или суперюзеров."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Чтение для всех.

    На изменение данных только для админа или суперюзера.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsOwnerAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Редактирование объекта.

    Только владельцы объекта, администраторы или модераторы.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False
        user = request.user
        return user.is_authenticated and (
            user == obj.author
            or user.is_admin
            or user.is_moderator
        )
