from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True

        owner = getattr(obj, 'owner', None)
        if owner is None and hasattr(obj, 'course'):
            owner = obj.course.owner

        return owner == request.user