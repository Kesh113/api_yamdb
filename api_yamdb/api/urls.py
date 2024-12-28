from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet, GenreViewSet, TitleViewSet, ReviewViewSet,
    CommentViewSet, UsersView, signup_or_update, confirmation
)


v1_router = DefaultRouter()
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)'
                   r'/reviews/(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
v1_router.register(r'users', UsersView, basename='users')

auth_urls = [
    path('v1/auth/signup/', signup_or_update, name='signup'),
    path('v1/auth/token/', confirmation, name='token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
] + auth_urls
