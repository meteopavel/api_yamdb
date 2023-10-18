from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    AdminUserViewSet,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    RegisterViewSet,
    ReviewViewSet,
    TitleViewSet,
    TokenJWTViewSet,
    UserProfileView,
)

v1_router = DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
v1_router.register('users', AdminUserViewSet, basename='users')

auth_patterns = [
    path(
        'signup/',
        RegisterViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        TokenJWTViewSet.as_view({'post': 'create'}),
        name='get-jwt-token'
    )
]

urlpatterns = [
    path('v1/users/me/', UserProfileView.as_view(), name='user-profile'),
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(v1_router.urls)),
]
