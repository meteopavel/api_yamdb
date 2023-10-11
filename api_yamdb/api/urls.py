from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, ReviewViewSet
from .views import (
    AdminUserViewSet,
    CategoryViewSet,
    GenreViewSet,
    RegisterViewSet,
    TitleViewSet,
    TokenJWTViewSet,
    UserProfileView,
)


v1_router = DefaultRouter()

v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'titles', TitleViewSet)
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
v1_router.register(r'users', AdminUserViewSet)
v1_router.register(r'auth/signup', RegisterViewSet, basename='signup')
v1_router.register(r'auth/token', TokenJWTViewSet, basename='get-jwt-token')


urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
