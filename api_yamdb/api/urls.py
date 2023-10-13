from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (AdminUserViewSet, CategoryViewSet, GenreViewSet,
                       RegisterViewSet, TitleViewSet, TokenJWTViewSet,
                       UserProfileView, CommentViewSet, ReviewViewSet)

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
v1_router.register('auth/signup', RegisterViewSet, basename='signup')
v1_router.register('auth/token', TokenJWTViewSet, basename='get-jwt-token')


urlpatterns = [
    path('v1/users/me/', UserProfileView.as_view(), name='user-profile'),
    path('v1/', include(v1_router.urls)),
]
