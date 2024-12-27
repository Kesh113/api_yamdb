from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator
)


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=13, choices=ROLE_CHOICES, default='user'
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.username[:21]}, роль - {self.role}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = 'username',


User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(date.today().year)]
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)


# class GenreTitle(models.Model):
#     title = models.ForeignKey(Title, on_delete=models.CASCADE)
#     genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_review_per_title'
            ),
        )

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',)
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:20]
