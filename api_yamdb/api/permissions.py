from rest_framework import permissions
from users.models import MyUser

class IsAdmin(permissions.BasePermission):
    """
    Доступ только для администраторов.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ для чтения для всех, а для записи только для администраторов.
    """
    
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

class  IsOwnerAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Доступ на чтение для всех. Автор, администратор или модератор могут редактировать.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )

class IsAdminOrModerator(permissions.BasePermission):
    """
    Доступ только для администратора или модератора.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_moderator
        )
