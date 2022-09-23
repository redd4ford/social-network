from rest_framework import permissions

from domain.core.exceptions import UserNotAuthorizedError


class UserPermission(permissions.BasePermission):
    """ UserViewSet permissions. """

    message = UserNotAuthorizedError().message

    def has_permission(self, request, view) -> bool:
        """
        Check if a user is authorized to use methods.
        """
        if not request.user.is_authenticated:
            return False

        if view.action == 'list':
            return request.user.is_staff
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        elif view.action == 'get_user_activity_statistics':
            return request.user.is_staff
        else:
            return False
