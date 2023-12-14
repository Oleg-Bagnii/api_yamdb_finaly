from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminAndAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin'
                                                  or request.user.is_superuser)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAdminOrAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
        )