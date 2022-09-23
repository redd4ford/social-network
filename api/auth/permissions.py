from rest_framework import permissions
from rest_framework.request import Request


class CreateUserProfilePermissions(permissions.BasePermission):
    """ User sign up (model creation) permissions. """

    message = 'You are already authenticated. Please log out to register a new account.'

    def has_permission(self, request: Request, view) -> bool:
        """
        Check if user is authenticated and has permission to access endpoints.
        """
        if request.method == 'POST':
            """
            Restrict registration endpoint for authenticated users.
            """
            return not request.user.is_authenticated
        else:
            """
            Else return false, as this permission class is used for registration view so far.
            """
            return False
