from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView, name='signup'), # вьюхи еще не готовы
    path('token/', views.TokenView, name='token'),
    path('me/', views.MyUsersMeView, name='me'),

]
