from django.urls import include, path


urlpatterns = [
    path('v1/auth/', include('users.urls', namespace='users')), # перенаправление на урлы юзера для реги и получения токена Альбина*
]