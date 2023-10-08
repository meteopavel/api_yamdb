from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from api.serializers import CommentSerializer, ReviewSerializer
from reviews.permissions import IsAdminOrReadOnly
from reviews.models import Review, Title

ALLOWED_METHODS = ('get', 'post', 'patch', 'delete')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
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
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly,
    )
    http_method_names = ALLOWED_METHODS

    @property
    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title.reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title)
