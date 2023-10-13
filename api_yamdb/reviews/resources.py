from import_export import resources
from users.models import MyUser
from .models import (
    Title,
    Category,
    Genre,
    Review,
    Comment
)


class UserResource(resources.ModelResource):
    class Meta:
        model = MyUser


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Review


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment
