import re

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_pk')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=request.user).exists():
            raise ValidationError(
                'Должен быть только один отзыв от пользователя.'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class EditTitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    def to_representation(self, instance):
        return ReadOnlyTitleSerializer(instance).data

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True,
        default=0
    )
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserEditSerializer(UserSerializer):
    """Сериализатор для редактирования модели User."""

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.MAX_USERNAME_LENGTH_150,
    )
    email = serializers.EmailField(
        max_length=settings.MAX_STRING_LENGTH_254,
    )

    # Не понимаю, как вынести функцию. Мозг кипит)
    # Её надо отдельно куда-то? А как тогда аргументы передать?
    # re.sub вроде реализовал. А по остальному нужна подсказка или пример
    def validate_username(self, value):
        forbidden_characters = re.sub(r'^[\w.@+-]+\Z', '', value)
        if not forbidden_characters == '':
            raise serializers.ValidationError(
                f'Использование символов {forbidden_characters} запрещено.'
            )

        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использование "me" в качестве имени пользователя запрещено.'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Получение JWT-токена в обмен на username и confirmation code."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()
