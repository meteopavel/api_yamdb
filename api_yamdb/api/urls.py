from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ReviewViewSet, CommentViewSet
from reviews.views import GenreViewSet, CategoryViewSet, TitleViewSet
from users.views import AdminUserViewSet, RegisterViewSet, TokenJWTViewSet


v1_router = DefaultRouter()

v1_router.register(r'categories', CategoryViewSet)
v1_router.register(r'genres', GenreViewSet)
v1_router.register(r'titles', TitleViewSet)
v1_router.register(r'titles/(?P<title_pk>\d+)/reviews', ReviewViewSet,
                   basename='reviews')
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    CommentViewSet,
    basename='comments',
)
v1_router.register(r'users', AdminUserViewSet)
v1_router.register(r'register', RegisterViewSet)
v1_router.register(r'get-jwt-token', TokenJWTViewSet, basename='get-jwt-token')

#v1_router.register(r'users', MyUserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/', include('users.urls')),
#    path('v1/users/me/', MyUsersMeView.as_view(), name='me'),
]
