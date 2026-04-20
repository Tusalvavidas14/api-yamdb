from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Read-only доступ всем, изменение — только администратору.

    Совместимо и с кастомной ролью `role='admin'`, и с django-superuser/staff.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if not getattr(user, "is_authenticated", False):
            return False

        if (
            getattr(user, "is_superuser", False)
            or getattr(user, "is_staff", False)
        ):
            return True

        return getattr(user, "role", None) == "admin"


class IsAdmin(BasePermission):
    """Только администраторы имеют доступ."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
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
