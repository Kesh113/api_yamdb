from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .constants import ONLY_ONE_REVIEW
from reviews.models import Review, Comment, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name', 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all(),
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Получаем объект категории и сериализуем его
        category = instance.category
        representation['category'] = CategorySerializer(category).data

        # Получаем объекты жанров и сериализуем их
        genres = instance.genre.all()
        representation['genre'] = GenreSerializer(genres, many=True).data

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Review
        exclude = 'title',
        read_only_fields = 'id', 'author', 'pub_date'

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=user, title=title_id).exists():
            raise serializers.ValidationError(ONLY_ONE_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = 'id', 'author', 'text', 'pub_date'
