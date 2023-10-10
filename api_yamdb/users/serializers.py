from rest_framework import serializers
#from rest_framework.generics import get_object_or_404
#from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.validators import UniqueValidator

from users.models import MyUser

#from rest_framework import status
#from rest_framework.exceptions import ValidationError
#from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели MyUser."""

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = (
            'role',
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=MyUser.objects.all())
        ]
    )
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использование "me" в качестве имени пользователя запрещено.'
            )
        return value
    
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email'
        )

#class SignUpSerializer(serializers.ModelSerializer):
#    """
#    Сериализатор для регистрации новых пользователей.

#    Поля:
#    - username: Имя пользователя.
#    - email: Адрес электронной почты.

#    Валидация:
#    - Поле username не должно быть равным 'me'.
#    - Поля username и email должны быть уникальными.
#    """

#    username = serializers.RegexField(
#        regex=r'^[\w.@+-]+\Z',
#        required=True,
#        max_length=150
#    )
#    email = serializers.EmailField(
#        max_length=254,
#        required=True,
#    )

#    def validate_username(self, value):
#        if value.lower() == 'me':
#            raise serializers.ValidationError(
#                "Использование 'me' в качестве имени пользователя запрещено."
#            )
#        return value

#    def validate_unique(self, value):
#        username = value.get('username')
#        email = value.get('email')

#        if (MyUser.objects.filter(email=email)
#                .exclude(username=username).exists()):
#            raise serializers.ValidationError({'email': 'Email уже занят'})

#        if (MyUser.objects.filter(username=username)
#                .exclude(email=email).exists()):
#            raise serializers.ValidationError(
#                {'username': 'Имя пользователя уже занято'}
#            )

#        return value


#    class Meta:
#        model = MyUser
#        fields = ('email', 'username')


#class UserMeSerializer(UserSerializer):
#    """Сериализация данных для эндпоинта users/me/."""

#    role = serializers.ChoiceField(choices=['user', 'moderator', 'admin'],
#                                   default='user')
#    first_name = serializers.CharField(max_length=150, required=False)
#    last_name = serializers.CharField(max_length=150, required=False)

#    class Meta:
#        model = MyUser
#        fields = ('username', 'email', 'first_name',
#                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
