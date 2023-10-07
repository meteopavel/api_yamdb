from django.urls import include, path
from rest_framework import routers

from api.views import CommentViewSet, GroupViewSet, FollowViewSet, PostViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'posts/(?P<post_pk>\d+)/comments', CommentViewSet,
                   basename='comments')
v1_router.register('groups', GroupViewSet, basename='groups')
v1_router.register('follow', FollowViewSet, basename='follows')
v1_router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/', include('users.urls', namespace='users')), # перенаправление на урлы юзера для реги и получения токена Альбина*
    path('v1/users/', include('users.urls', namespace='users')), # перенаправление на урлы юзера для заполнения полей профиля Альбина*
]