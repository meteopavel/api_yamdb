from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.mixins import ListCreateDestroyViewSet
from reviews.models import Category, Genre, Review, Title
from users.models import User
from api.filters import TitlesFilter
from api.permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsOwnerAdminOrModeratorOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    CommentSerializer,
    ReviewSerializer,
    ReadOnlyTitleSerializer,
    TitleSerializer,
    TokenSerializer,
    UserEditSerializer,
    UserRegisterSerializer,
    UserSerializer
)

ALLOWED_METHODS = [
    'get',
    'post',
    'patch',
    'delete'
]


class CustomPagination(PageNumberPagination):
    page_size = 10


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    http_method_names = ALLOWED_METHODS

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminOrModeratorOrReadOnly
    )
    http_method_names = ALLOWED_METHODS

    @property
    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review.comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerAdminOrModeratorOrReadOnly,
    )
    http_method_names = ALLOWED_METHODS

    @property
    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_pk'))

    def get_queryset(self):
        return self.get_title.reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title)


class AdminUserViewSet(ModelViewSet):
    lookup_field = 'username'
    search_fields = ['username', 'email']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAdmin,
    )
    pagination_class = CustomPagination
    http_method_names = ALLOWED_METHODS


class RegisterViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        user_email = request.data.get('email')

        # Проверяем, существует ли уже пользователь с таким именем
        user = User.objects.filter(username=username).first()

        if not user:
            # Если пользователь не найден, создаем нового
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
        else:
            if user.email != user_email:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        # Создаем и отправляем код подтверждения
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Регистрация в YaMDb',
            message=f'Ваш одноразовый код: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email]
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
