from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly


ALLOWED_METHODS = (
    'get',
    'post',
    'patch',
    'delete'
)


class CategoryGenreBaseViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'


class BaseViewSet(ModelViewSet):
    """
    Базовый вьюсет, который ограничивает доступные методы
    """
    http_method_names = ALLOWED_METHODS
