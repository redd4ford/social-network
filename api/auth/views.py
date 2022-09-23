from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.auth.permissions import CreateUserProfilePermissions
from api.auth.serializers import (
    RegisterInputSerializer,
    RegisterOutputSerializer,
    LogoutInputSerializer,
)
from rest_framework.generics import CreateAPIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_205_RESET_CONTENT,
    HTTP_400_BAD_REQUEST,
)


class SignUpAPIView(CreateAPIView):
    """ User sign up view. """

    serializer_class = RegisterInputSerializer
    permission_classes = (CreateUserProfilePermissions,)
    authentication_classes = (JWTAuthentication,)

    @extend_schema(
        request=RegisterInputSerializer,
        responses={
            200: OpenApiResponse(
                description='Registration successful',
                response=RegisterOutputSerializer
            ),
            400: OpenApiResponse(description='Bad request')
        },
    )
    def post(self, request, *args,  **kwargs):
        """
        Register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                'user': RegisterOutputSerializer(user, context=self.get_serializer_context()).data,
                'message': 'Registration was successful. '
                           'Please login to obtain access to the social network.',
            },
            status=HTTP_200_OK
        )


class SignOutAPIView(CreateAPIView):
    """ User sign out view. """

    serializer_class = LogoutInputSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    @extend_schema(
        request=LogoutInputSerializer,
        responses={
            205: OpenApiResponse(description='Logout successful'),
            400: OpenApiResponse(description='Bad request'),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Log the user out with their refresh token. The token will be then blacklisted.
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            token = RefreshToken(serializer.data['refresh'])
            token.blacklist()

            return Response(
                {'message': 'Logout successful.'},
                status=HTTP_205_RESET_CONTENT
            )
        except TokenError as e:
            return Response(
                {'message': f'{e}'},
                status=HTTP_400_BAD_REQUEST
            )
