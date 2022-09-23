from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
)
from injector import inject
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.analytics.serializers import LikeAnalyticsOutputSerializer
from app_services import LikeAnalyticsService


class LikeAnalyticsViewSet(ViewSet):
    """ Like analytics view. """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def __init__(self, service: LikeAnalyticsService = LikeAnalyticsService(), **kwargs):
        super(LikeAnalyticsViewSet, self).__init__(**kwargs)
        self.service = service

    def dispatch(self, request, *args, **kwargs):
        return super(LikeAnalyticsViewSet, self).dispatch(request, *args, **kwargs)

    @inject
    def setup(
            self, request, service: LikeAnalyticsService = LikeAnalyticsService(),
            *args, **kwargs
    ):
        super(LikeAnalyticsViewSet, self).setup(request, service, args, kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'username',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description='Filter likes by username (case-sensitive).',
            ),
            OpenApiParameter(
                'post_title',
                OpenApiTypes.STR,
                OpenApiParameter.QUERY,
                description='Filter likes by post title (case-sensitive).',
            ),
            OpenApiParameter(
                'date_from',
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description='Filter likes performed STARTING FROM date_from '
                            'in a format: YYYY-MM-DD.',
            ),
            OpenApiParameter(
                'date_to',
                OpenApiTypes.DATE,
                OpenApiParameter.QUERY,
                description='Filter like operations performed BEFORE date_to in a format: '
                            'YYYY-MM-DD. If date_from = date_to, it will return all the like '
                            'operations performed in that exact day.',
            ),
        ],
        request=None,
        responses={200: LikeAnalyticsOutputSerializer(many=True)},
    )
    def list(self, request):
        analytics = self.service.get_like_analytics(query_params=request.query_params)

        output_serializer = LikeAnalyticsOutputSerializer(analytics, many=True)
        return Response(output_serializer.data, status=HTTP_200_OK)
