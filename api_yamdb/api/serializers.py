from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.constants import (
    ONLY_ONE_REVIEW, MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
)
from reviews.models import (
    Review, Comment, Category, Genre, Title
)


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name', 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleWriteSerializer(serializers.ModelSerializer):
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
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)

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
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

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


class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    confirmation_code = serializers.CharField(required=True)

    def validate_username(self, value):
        User._meta.get_field('username').validators[0](value)
        return value


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )

    def validate_username(self, value):
        User._meta.get_field('username').validators[0](value)
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        User._meta.get_field('username').validators[0](value)
        return value


class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = 'role',
