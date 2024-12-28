from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Category, Comment, Genre, Review, Title


User = get_user_model()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ('name', 'slug')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'pub_date')
    list_filter = ('author', 'review')
    search_fields = ('author__username', 'review__title__name')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('author', 'title')
    search_fields = ('author__username', 'title__name')


class ReviewsUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    list_filter = ('username',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category')
    list_filter = ('genre', 'category')
    search_fields = ('name', 'genre__name', 'category__name')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(User, ReviewsUserAdmin)
admin.site.register(Title, TitleAdmin)
