import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import (
    IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly, IsAdmin
)
from .filters import TitleFilter
from .serializers import (
    ReviewSerializer, CommentSerializer, CategorySerializer, GenreSerializer,
    TitleReadSerializer, TitleWriteSerializer, UserSerializer,
    UserProfileSerializer, UserSignupSerializer, UserConfirmationSerializer
)
from reviews.constants import MESSAGE, SUBJECT
from reviews.models import Title, Genre, Category, Review


User = get_user_model()

INVALID_CONFIRM_CODE = 'Неверный код подтверждения.'

ALREADY_EXIST_FIELD = 'Этот {} уже занят.'


class CategoryGenreBaseViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = IsAdminOrReadOnly,
    filter_backends = filters.SearchFilter,
    search_fields = 'name',
    pagination_class = PageNumberPagination
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by(*Title._meta.ordering)
    permission_classes = IsAdminOrReadOnly,
    filter_backends = DjangoFilterBackend, filters.OrderingFilter
    filterset_class = TitleFilter
    pagination_class = PageNumberPagination
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )
    pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )
    pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UsersView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )
    lookup_field = 'username'
    filter_backends = filters.SearchFilter,
    search_fields = 'role', 'username'
    permission_classes = IsAdmin,
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path=settings.USERNAME_RESERVED,
        permission_classes=(IsAuthenticated,)
    )
    def user_profile(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = UserProfileSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_or_update(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    try:
        user, _ = User.objects.get_or_create(**data)
    except IntegrityError:
        if User.objects.filter(username=data['username']).exists():
            raise ValidationError(
                {'username': ALREADY_EXIST_FIELD.format('username')}
            )
        elif User.objects.filter(email=data['email']).exists():
            raise ValidationError(
                {'email': ALREADY_EXIST_FIELD.format('email')}
            )
    # Генерируем код подтверждения и сохраняем пользователю
    confirmation_code = ''.join(random.choices(
        settings.VALID_CHARS_CODE,
        k=settings.LENGTH_CODE)
    )
    user.confirmation_code = confirmation_code
    user.save()
    # Отправляем код подтверждения по электронной почте
    send_mail(
        subject=SUBJECT,
        message=MESSAGE.format(confirmation_code),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[data['email']]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def confirmation(request):
    serializer = UserConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    user = get_object_or_404(User, username=data['username'])
    # Проверяем генерировался ли код для пользователя
    if user.confirmation_code == settings.RESERVED_CODE:
        raise ValidationError({'confirmation_code': INVALID_CONFIRM_CODE})
    # Отбираем возможность повторной проверки кода
    confirmation_code = user.confirmation_code
    if user.confirmation_code != settings.RESERVED_CODE:
        user.confirmation_code = settings.RESERVED_CODE
        user.save()
    # Если код подтверждения совпал генерируем токен пользователю
    if confirmation_code != data['confirmation_code']:
        raise ValidationError({'confirmation_code': INVALID_CONFIRM_CODE})
    return Response(
        {'token': str(AccessToken.for_user(user))}, status=status.HTTP_200_OK
    )
