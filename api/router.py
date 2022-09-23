from django.conf import settings
from django.conf.urls.static import static
from django.urls import (
    path,
    include,
)
from rest_framework_nested import routers
from rest_framework_simplejwt import views as jwt_views

from api.analytics import LikeAnalyticsViewSet
from api.auth import (
    SignUpAPIView,
    SignOutAPIView,
)
from api.users import UserViewSet
from api.posts import PostViewSet
from api.likes import LikeViewSet

router = routers.SimpleRouter()

# Users
router.register(r'users', UserViewSet, basename='users')

# Posts
router.register(r'posts', PostViewSet, basename='posts')
posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post', trailing_slash=False)
posts_router.register(r'react', LikeViewSet, basename='post_react')

# Analytics
router.register(r'analytics', LikeAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(posts_router.urls)),

    # Authentication
    path('auth/register/', SignUpAPIView.as_view(), name='auth_register'),
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='auth_token_obtain_pair'),
    path('auth/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('auth/logout/', SignOutAPIView.as_view(), name='auth_logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
