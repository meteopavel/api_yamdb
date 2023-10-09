
from api.permissions import IsAdminFullAccess
from users.serializers import SignUpSerializer, TokenSerializer, UserSerializer, UserMeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import MyUser
from rest_framework.exceptions import ValidationError

from users.forms import send_confirmation_code


class MyUserViewSet(ModelViewSet):
    """
    Вьюсет для модели MyUser.

    Для работы с пользователями (удаление, корректировка и т.д.).
    """

    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated, IsAdminFullAccess,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')


class MyUsersMeView(APIView):
    """
    Вью для эндпоинта users/me/.

    После регистрации и получения токена пользователь может отправить
    PATCH-запрос на эндпоинт /api/v1/users/me/
    и заполнить поля в своём профиле.
    """

    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        me = get_object_or_404(MyUser, username=request.user.username)
        serializer = UserMeSerializer(me, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # Проверка длины last_name
        last_name = serializer.validated_data.get('last_name')
        if last_name and len(last_name) > 150:
            raise ValidationError({'last_name': 'Фамилия не должна превышать 150 символов.'})

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class TokenView(TokenObtainPairView):
    """Вью для получения токена."""

    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer


class SignupView(APIView):
    """Вью для регистрации пользователей."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Метод POST."""
        serializer = SignUpSerializer(data=request.data)
        if MyUser.objects.filter(username=request.data.get('username'),
                                 email=request.data.get('email')).exists():
            send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)
