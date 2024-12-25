from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

# from api.permissions import Admin
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Title


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(reviews__score))
    serializer_class = TitleSerializer
    # permission_classes = (Admin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
