from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminPermission(BasePermission):
    """Только администраторы имеют доступ."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnlyPermission(IsAdminPermission):
    """
    Read-only доступ всем, изменение — только администратору.

    Совместимо и с кастомной ролью `role='admin'`, и с django-superuser/staff.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )

class IsAuthorModeratorAdminOrReadOnlyPermission(BasePermission):
    """Изменение доступно автору, модератору и администратору."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
