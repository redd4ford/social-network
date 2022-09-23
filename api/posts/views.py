from django.core.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from injector import inject
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ViewSet

from api.posts.serializers import (
    PostOutputSerializer,
    PostInputSerializer,
    PostUpdateSerializer,
)
from app_services import PostService
from domain.core.exceptions import ObjectDoesNotExistError


class PostViewSet(ViewSet):
    """ Post CRUD view. """

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def __init__(self, service: PostService = PostService(), **kwargs):
        super(PostViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(PostViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: PostService = PostService(),
            *args, **kwargs
    ):
        super(PostViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[OpenApiParameter('id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Resource not found'),
        },
    )
    def retrieve(self, request, pk):
        """
        Get Post by id.
        """
        try:
            post = self.service.get_by_id(pk)

            output_serializer = PostOutputSerializer(post)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)

    @extend_schema(
        parameters=[OpenApiParameter('user_id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer(many=True)),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    @action(methods=['get'], detail=False, url_path='by-user/(?P<user_pk>[^/.]+)')
    def get_by_user(self, request, user_pk):
        """
        Get all Posts created by a User with specified user_id.
        """
        posts = self.service.get_by_user(user_pk)

        output_serializer = PostOutputSerializer(posts, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer(many=True)),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    def list(self, request):
        """
        Get all Posts.
        """
        posts = self.service.get_all()

        output_serializer = PostOutputSerializer(posts, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)

    @extend_schema(
        parameters=None,
        request=PostInputSerializer,
        responses={
            201: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description="Bad request"),
        },
    )
    def create(self, request):
        """
        Create Post.
        """
        incoming_data = PostInputSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            post = self.service.create(request.user, incoming_data.validated_data)

            output_serializer = PostOutputSerializer(post)
            return Response(output_serializer.data, status=HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter('id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=PostUpdateSerializer,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Resource not found'),
        },
    )
    def update(self, request, pk):
        """
        Update Post.
        """
        incoming_data = PostUpdateSerializer(data=request.data)
        incoming_data.is_valid(raise_exception=True)

        try:
            post = self.service.update(request.user, pk, incoming_data.validated_data)

            output_serializer = PostOutputSerializer(post)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[OpenApiParameter('id', OpenApiTypes.UUID, OpenApiParameter.PATH)],
        request=None,
        responses={
            200: OpenApiResponse(response=PostOutputSerializer),
            400: OpenApiResponse(description='Bad request'),
            404: OpenApiResponse(description='Resource not found')
        },
    )
    def destroy(self, request, pk):
        """
        Delete Post.
        """
        try:
            deleted_post = self.service.delete(request.user, pk)

            output_serializer = PostOutputSerializer(deleted_post)
            return Response(output_serializer.data, status=HTTP_200_OK)
        except ObjectDoesNotExistError as e:
            return Response({'message': e.message}, status=HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'message': e.message}, status=HTTP_400_BAD_REQUEST)
