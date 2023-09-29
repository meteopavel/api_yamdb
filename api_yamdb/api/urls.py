from django.urls import include, path


urlpatterns = [
    path('v1/auth/', include('users.urls', namespace='users')), # перенаправление на урлы юзера для реги и получения токена Альбина*
    path('v1/users/', include('users.urls', namespace='users')), # перенаправление на урлы юзера для заполнения полей профиля Альбина*
]