from django.urls import include, path
from rest_framework import routers

from api.views import ReviewViewSet, CommentViewSet
from reviews.views import GenreViewSet, CategoryViewSet, TitleViewSet
from users.views import MyUserViewSet


v1_router = routers.DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_pk>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
v1_router.register('users', MyUserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/', include('users.urls')),
]
