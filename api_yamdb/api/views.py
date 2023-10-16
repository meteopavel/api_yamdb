from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .mixins import BaseViewSet, CategoryGenreBaseViewSet
from .filters import TitlesFilter
from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsOwnerAdminOrModeratorOrReadOnly
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenSerializer,
    UserEditSerializer,
    UserRegisterSerializer,
    UserSerializer
)
from reviews.models import Category, Genre, Review, Title
from users.models import User


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(BaseViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CommentViewSet(BaseViewSet):
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


class ReviewViewSet(BaseViewSet):
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


class AdminUserViewSet(BaseViewSet):
    lookup_field = 'username'
    search_fields = ['username', 'email']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAdmin,
    )


class RegisterViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        user_email = request.data.get('email')

        # Получаем пользователя по email и username
        user_by_email = User.objects.filter(email=user_email).first()
        user_by_username = User.objects.filter(username=username).first()

        # Проверяем результаты
        if (user_by_email and user_by_username
                and user_by_email != user_by_username):
            return Response(
                data={
                    'detail': 'email и username не соответствуют одному user.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Если пользователь с таким именем не найден, создаем нового
        if not user_by_username:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        else:
            if user_by_username.email != user_email:
                return Response(
                    data={
                        'detail': 'Email не соответствует указанному username.'
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Создаем и отправляем код подтверждения
        confirmation_code = default_token_generator.make_token(
            user_by_username or user
        )
        send_mail(
            subject='Регистрация в YaMDb',
            message=f'Ваш одноразовый код: {confirmation_code}',
            from_email=None,
            recipient_list=[user_email]
        )

        return Response(
            {'username': username, 'email': user_email},
            status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserEditSerializer

    def get(self, request, format=None):
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
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenJWTViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

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
