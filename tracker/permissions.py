from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and getattr(request.user, "is_staff", None)
        )


class IsAssigneeOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            print(f"Request method is safe {request.method}")
            return True

        return request.user.is_authenticated and (
            getattr(request.user, "is_staff", None)
            or getattr(obj, "assignee_id", None) == request.user.id
        )
