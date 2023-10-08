from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework.exceptions import ValidationError

from reviews.models import Comment, Review, Title


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
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1,
                'Рейтинг не может быть ниже 10'
            ),
            MaxValueValidator(
                10,
                'Рейтинг не может быть выше 10'
            ),
        )
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if Review.objects.filter(title=title, author=request.user).exists():
            raise ValidationError('Должен быть только один отзыв.')
        return data

    class Meta:
        fields = '__all__'
        model = Review
