
#from api.permissions import IsAdminFullAccess
from users.serializers import (
    TokenSerializer,
    UserSerializer,
    UserEditSerializer,
    UserRegisterSerializer
)
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
#from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import MyUser
#from rest_framework.exceptions import ValidationError


#from users.forms import send_confirmation_code
from users.permissions import IsAdmin


#class MyUserViewSet(ModelViewSet):
#    """
#    Вьюсет для модели MyUser.

#    Для работы с пользователями (удаление, корректировка и т.д.).
#    """

#    queryset = MyUser.objects.all()
#    permission_classes = (IsAdmin,)
#    serializer_class = UserSerializer
#    lookup_field = 'username'
#    http_method_names = ('get', 'post', 'patch', 'delete')

class AdminUserViewSet(ModelViewSet):
    lookup_field = 'username'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAdmin,
    )


class RegisterViewSet(GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            MyUser,
            username=serializer.valid
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация в YaMDb',
            message=f'Ваш одноразовый код: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email]
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserEditSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenJWTViewSet(GenericViewSet):
    queryset = MyUser.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            MyUser,
            username=serializer.validated_data['username']
        )

        if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#class TokenView(TokenObtainPairView):
#    """Вью для получения токена."""

#    permission_classes = (AllowAny,)
#    serializer_class = TokenSerializer


#class SignupView(APIView):
#    """Вью для регистрации пользователей."""

#    permission_classes = (AllowAny,)

#    def post(self, request):
#        """Метод POST."""
#        serializer = SignUpSerializer(data=request.data)
#        if MyUser.objects.filter(username=request.data.get('username'),
#                                 email=request.data.get('email')).exists():
#            send_confirmation_code(request)
#            return Response(request.data, status=status.HTTP_200_OK)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()
#        send_confirmation_code(request)
#        return Response(serializer.data, status=status.HTTP_200_OK)
