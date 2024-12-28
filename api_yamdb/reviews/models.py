from datetime import date

from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from api.constants import MAX_SCORE, MAX_STR_LEN



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


class ReviewCommentAbstract(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_STR_LEN]



class Review(ReviewCommentAbstract):
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(MAX_SCORE,)])
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_review_per_title'
            ),
        )


class Comment(ReviewCommentAbstract):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

