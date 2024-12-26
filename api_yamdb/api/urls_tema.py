from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views_auth import signup_or_update, confirmation
from .views_users import user_profile, UsersView


router_v1 = DefaultRouter()
router_v1.register('users', UsersView, basename='users')


urlpatterns = [
    path('v1/auth/signup/', signup_or_update, name='signup'),
    path('v1/auth/token/', confirmation, name='token'),
    path('v1/users/me/', user_profile, name='profile'),
    path('v1/', include(router_v1.urls)),
]
