from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .constants import (
    INVALID_CONFIRM_CODE, ONLY_ONE_REVIEW,
    MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
)
from reviews.models import (
    Review, Comment, Category, Genre, Title, UsernameValidator
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


class UserConfirmationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        UsernameValidator()(value)
        return value

    def validate(self, data):
        data['user'] = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            data['user'], data['confirmation_code']
        ):
            raise serializers.ValidationError(INVALID_CONFIRM_CODE)
        return data


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )

    def validate_username(self, value):
        UsernameValidator()(value)
        return value

    def validate(self, data):
        try:
            data['user'], _ = User.objects.get_or_create(**data)
        except IntegrityError as e:
            raise serializers.ValidationError(e)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        UsernameValidator()(value)
        return value


class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = 'role',
