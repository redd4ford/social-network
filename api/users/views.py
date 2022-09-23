from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from injector import inject
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ViewSet

from api.users.permissions import UserPermission
from api.users.serializers import UserActivityStatSerializer
from app_services.user import UserService
from domain.core.exceptions import ObjectDoesNotExistError


class UserViewSet(ViewSet):
    """ User view. """

    permission_classes = (UserPermission,)

    def __init__(
            self, service: UserService = UserService(),
            **kwargs
    ):
        super(UserViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(UserViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: UserService = UserService(),
            *args, **kwargs
    ):
        super(UserViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter('id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=UserActivityStatSerializer),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Resource not found'),
        },
    )
    @action(methods=['get'], detail=True, url_path='activity-stat')
    def get_user_activity_statistics(self, request, pk):
        """
        Retrieve user activity statistics by their id (last login time and when they made a last
        request to the service. This endpoint is to be used by the staff only.
        """
        try:
            user = self.service.get_by_id(pk)

            output_serializer = UserActivityStatSerializer(user)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)
