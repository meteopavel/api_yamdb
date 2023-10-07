from django.urls import path
from users.views import SignupView, TokenView, MyUsersMeView

urlpatterns = [
    path('signup/', SignupView, name='signup'),  # вьюхи еще не готовы
    path('token/', TokenView, name='token'),
    path('me/', MyUsersMeView, name='me'),
]
