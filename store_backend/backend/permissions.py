from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """Custom permission to only allow the user to edit their own information, or admins to edit others."""

    def has_permission(self, request, view):
        # Allow access if user is admin or the action is 'list' and user is admin
        if view.action == 'list':
            return request.user.is_staff
        return True

    def has_object_permission(self, request, view, obj):
        # Allow full access to admins or if the request is to the user's own data
        return request.user.is_staff or obj == request.user