from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


@admin.register(User)
class CustomUserAdmin(ModelAdmin):
    exclude = ('password', 'last_login', 'is_staff', 'is_active',
               'date_joined', 'groups', 'user_permissions')


admin.site.register([Genre, Category, Title, Review, Comment])
