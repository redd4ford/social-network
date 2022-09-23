from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.utils.timezone import now

from app_services.user import UserService


User = get_user_model()


class SetLastRequestTimeMiddleware:
    """
    Update last visit time after request finished processing.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if request.user.is_authenticated:
            UserService().update(
                user_id=request.user.pk,
                data={'last_request_time': now()}
            )

        response = self.get_response(request)

        return response
