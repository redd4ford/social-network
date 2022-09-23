from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
)
from injector import inject
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.posts.serializers import PostOutputSerializer
from app_services import LikeService
from domain.core.exceptions import (
    LikeAlreadyExistsError,
    LikeDoesNotExistError,
)


class LikeViewSet(ViewSet):
    """ Likes/Unlikes view. """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def __init__(self, service: LikeService = LikeService(), **kwargs):
        super(LikeViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(LikeViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: LikeService = LikeService(),
            *args, **kwargs
    ):
        super(LikeViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter('post_id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    @action(methods=['post'], detail=False, url_path='like')
    def like(self, request, post_pk):
        """
        Like the Post.
        """
        try:
            liked = self.service.like(request.user, post_pk)

            output_serializer = PostOutputSerializer(liked.post)
            return Response(output_serializer.data, status=HTTP_201_CREATED)
        except LikeAlreadyExistsError as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter('post_id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    @action(methods=['delete'], detail=False, url_path='unlike')
    def unlike(self, request, post_pk):
        """
        Unlike the Post.
        """
        try:
            unliked = self.service.unlike(request.user, post_pk)

            output_serializer = PostOutputSerializer(unliked.post)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except LikeDoesNotExistError as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)
