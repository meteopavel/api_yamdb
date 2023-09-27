from rest_framework import permissions


class IsAuthorOrReadOnlyOrAdminOrModerator(permissions.BasePermission):
    """
    Если аноним - доступ только на чтение.

    Если юзер является автором объекта, то может удалять, менять его.
    Если админ или модератор - могут удалять, редактировать все объекты.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
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
                and request.user.is_admin)
        )



class IsAdminOrSuperuserOrStaff(permissions.BasePermission):
    """
    Доступ только для администратора или суперюзера.
    
    Для анонимов и юзеров - доступ закрыт.
    
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin
            or request.user.is_superuser
            or request.user.is_staff
        )
