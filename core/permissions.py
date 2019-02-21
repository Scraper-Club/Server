from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object level permission to allow
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
