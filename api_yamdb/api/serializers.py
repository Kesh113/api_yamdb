from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.constants import (
    MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
)
from reviews.models import (
    Review, Comment, Category, Genre, Title
)


User = get_user_model()

ONLY_ONE_REVIEW = 'Можно оставить только один отзыв на произведение'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    # FIX
    # rating = serializers.IntegerField(read_only=True)
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
        fields = (
            'id', 'name', 'year',
            # FIX
            # 'rating',
            'description', 'genre', 'category'
        )

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        print('1  ', repr)
        # Все на месте, ratings на месте, можно возращать.
        # А работает все, как надо, потому что для получения данных
        # self.get_queryset используется, а там у нас живет аннотация.
        data = TitleReadSerializer(instance).data
        print('2  ', data)
        return data

    # def to_representation(self, instance):
    #     repr = s
    #     return TitleReadSerializer(instance).data


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


class ValidateUsernameMixin:
    def validate_username(self, value):
        for validator in User._meta.get_field('username').validators:
            validator(value)
        return value


class UserConfirmationSerializer(
    serializers.Serializer, ValidateUsernameMixin
):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LENGTH_CODE, required=True
    )


class UserSignupSerializer(serializers.Serializer, ValidateUsernameMixin):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME, required=True
    )
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL, required=True)


class UserSerializer(serializers.ModelSerializer, ValidateUsernameMixin):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserProfileSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = 'role',
