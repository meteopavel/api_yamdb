from rest_framework import filters, mixins, permissions, viewsets


class CommentViewSet(viewsets.ModelViewSet):
    pass


class FollowViewSet(viewsets.ModelViewSet):
    pass


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    pass


class PostViewSet(viewsets.ModelViewSet):
    pass