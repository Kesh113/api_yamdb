from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .constants import PARAMETRS
from .permissions import IsAdminModeratorAuthorOrReadOnly, IsAdminOrReadOnly

from .serializers import (ReviewSerializer,
                          CommentSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          TitleSerializer)
from reviews.models import (Title,
                            Genre,
                            Category,
                            Review)

User = get_user_model()


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = IsAdminOrReadOnly,
    filter_backends = filters.SearchFilter,
    pagination_class = PageNumberPagination
    search_fields = 'name',
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = IsAdminOrReadOnly,
    filter_backends = filters.SearchFilter,
    pagination_class = PageNumberPagination
    search_fields = 'name',
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    filter_backends = filters.SearchFilter, filters.OrderingFilter
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly,
    pagination_class = PageNumberPagination
    http_method_names = (
        'get', 'post', 'patch', 'delete', 'head', 'options', 'trace'
    )




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
