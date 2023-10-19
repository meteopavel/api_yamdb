from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api.mixins import (GetPostPatchDeleteBaseViewSet,
                        CategoryGenreBaseViewSet)
from api.filters import TitlesFilter
from api.permissions import (IsAdmin, IsAdminOrReadOnly,
                             IsOwnerAdminOrModeratorOrReadOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReadOnlyTitleSerializer,
                             ReviewSerializer, EditTitleSerializer,
                             TokenSerializer, UserEditSerializer,
                             UserRegisterSerializer, UserSerializer)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(GetPostPatchDeleteBaseViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = EditTitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return EditTitleSerializer


class CommentViewSet(GetPostPatchDeleteBaseViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminOrModeratorOrReadOnly
    )

    @property
    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review.comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review)


class ReviewViewSet(GetPostPatchDeleteBaseViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminOrModeratorOrReadOnly,
    )

    @property
    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_pk'))

    def get_queryset(self):
        return self.get_title.reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title)


class AdminUserViewSet(GetPostPatchDeleteBaseViewSet):
    lookup_field = 'username'
    search_fields = ('username', 'email')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(detail=False,
            methods=('get', 'patch',),
            permission_classes=(IsAuthenticated,),
            serializer_class=UserEditSerializer)
    def me(self, request, format=None):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.serializer_class(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        user_email = request.data.get('email')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Получаем пользователя по email и username
        user_by_email = User.objects.filter(email=user_email).first()
        user_by_username = User.objects.filter(username=username).first()

        # Проверяем результаты
        if (user_by_email != user_by_username):
            return Response(
                data={
                    'detail': 'email и username не совпадают ни с одним user.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user, created = User.objects.get_or_create(
            email=user_email,
            username=username)

        # Создаем и отправляем код подтверждения
        confirmation_code = default_token_generator.make_token(
            user_by_username or user
        )
        send_mail(
            subject='Регистрация в YaMDb',
            message=f'Ваш одноразовый код: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=(user_email,)
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenJWTViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )

        if default_token_generator.check_token(
            user,
            serializer.validated_data['confirmation_code']
        ):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
