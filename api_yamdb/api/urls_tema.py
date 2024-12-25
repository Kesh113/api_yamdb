from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views_users import user_profile

from .views_auth import signup_or_update, confirmation


router_v1 = DefaultRouter()
# router_v1.register('me', UserProfileView, basename='profile')
# router_v1.register('signup', signup_or_update, basename='signup')
# router_v1.register('token', confirmation, basename='token')

urlpatterns = [
    path('v1/auth/signup/', signup_or_update, name='signup'),
    path('v1/auth/token/', confirmation, name='token'),
    # path('v1/users/', include(router_v1.urls))
    path('v1/users/me/', user_profile, name='profile'),
    # path('v1/auth/', include(router_v1.urls))
]
