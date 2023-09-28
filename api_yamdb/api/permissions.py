from rest_framework import permissions
from users.models import MyUser


class IsAuthorOrReadOnlyOrAdminOrModerator(permissions.BasePermission):
    """
    Если аноним - доступ только на чтение.

    Если юзер является автором объекта, то может удалять, менять его.
    Если админ или модератор - могут удалять, редактировать все объекты.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == MyUser.USER
            or request.user.role in (MyUser.ADMIN, MyUser.MODERATOR, )
        )

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)


class IsAdminFullAccess(permissions.BasePermission):
    """
    Доступ только для администратора.

    Если анонин - только чтение.
    """

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role in (MyUser.ADMIN,))
        )


class IsAdminOrSuperuserOrStaff(permissions.BasePermission):
    """
    Доступ только для администратора или суперюзера.

    Для анонимов и юзеров - доступ закрыт.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role in (MyUser.ADMIN, MyUser.MODERATOR,)
        )
