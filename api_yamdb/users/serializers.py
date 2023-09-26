from rest_framework import serializers

from users.models import MyUser


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели MyUser."""

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = MyUser


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации новых пользователей.

    Поля:
    - username: Имя пользователя (соответствует username в модели).
    - email: Адрес электронной почты (соответствует email в модели).

    Валидация:
    - Поле username не должно быть равным 'me'.
    - Поля username и email должны быть уникальными.

    Параметры:
    - max_length: Максимальная длина для полей 'username' и 'email'.
    """

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использование 'me' в качестве имени пользователя запрещено."
            )
        return value

    def validate_unique(self, value):
        username = value.get('username')
        email = value.get('email')

        if (MyUser.objects.filter(email=email)
                .exclude(username=username).exists()):
            raise serializers.ValidationError({'email': 'Email уже занят'})

        if (MyUser.objects.filter(username=username)
                .exclude(email=email).exists()):
            raise serializers.ValidationError(
                {'username': 'Имя пользователя уже занято'}
            )

        return value

    class Meta:
        model = MyUser
        fields = ('email', 'username')


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150
    )
    confirmation_code = serializers.CharField(
        required=True
    )
