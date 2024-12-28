from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response

from .constants import INVALID_CONFIRM_CODE, ONLY_ONE_REVIEW, MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
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
    rating = serializers.SerializerMethodField()
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

    def get_rating(self, obj):
        reviews = obj.reviews.all()

        if reviews:
            rating = [review.score for review in reviews]
            return sum(rating) // len(rating)

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
        if self.context.get('request').method == 'POST':
            author = self.context.get('request').user
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(author=author, title=title_id).exists():
                raise serializers.ValidationError(ONLY_ONE_REVIEW)
            if not Title.objects.filter(pk=title_id).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = 'id', 'author', 'text', 'pub_date'
        read_only_fields = 'id',

    def validate(self, data):
        title_id = self.context.get('view').kwargs.get('title_id')
        if not Title.objects.filter(pk=title_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return data


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
