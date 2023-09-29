from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views, name='signup'), # вьюхи еще не готовы
    path('token/', views, name='token'),
    path('me/', views, name='me'),

]
