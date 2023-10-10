from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from users.views import SignupView, TokenView, MyUsersMeView
from .views import AdminUserViewSet, UserProfileView, RegisterViewSet, TokenJWTViewSet



#urlpatterns = [
#    path('signup/', SignupView, name='signup'),  # вьюхи еще не готовы
#    path('token/', TokenView, name='token'),
#]
router = DefaultRouter()
router.register(r'users', AdminUserViewSet)
router.register(r'register', RegisterViewSet)
router.register(r'get-jwt-token', TokenJWTViewSet, basename='get-jwt-token')

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
