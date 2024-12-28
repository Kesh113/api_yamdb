from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy

from api.constants import (
    ADMIN_ROLE, MAX_LENGTH_EMAIL, MAX_LENGTH_FIRST_LAST_NAME,
    MODERATOR_ROLE, USER_ROLE, USERNAME_BAN, MAX_LENGTH_USERNAME
)


ROLE_CHOICES = (
    (USER_ROLE, 'Пользователь'),
    (MODERATOR_ROLE, 'Модератор'),
    (ADMIN_ROLE, 'Администратор')
)

USER_ALREADY_EXIST = 'Пользователь с таким username уже существует.'

USERNAME_HELP_TEXT = ('Обязательное поле. Не более 150 символов. Только буквы,'
                      f' цифры и @/./+/-/_. Слова кроме "{USERNAME_BAN}".')

USERNAME_VALIDATE_MASSAGE = (
    'Введите действительное имя пользователя. '
    'Это значение может содержать только буквы '
    f'числа, и символы: @/./+/-/_ . Слова кроме "{USERNAME_BAN}".'
)

MAX_LENGTH_ROLE = max(map(lambda role: len(role[0]), ROLE_CHOICES))


@deconstructible
class UsernameValidator(RegexValidator):
    regex = rf'^(?!{USERNAME_BAN}$)[\w.@+-]+\Z'
    message = gettext_lazy(USERNAME_VALIDATE_MASSAGE)


class ReviewsUser(AbstractUser):
    email = models.EmailField(max_length=MAX_LENGTH_EMAIL, unique=True)
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        help_text=gettext_lazy(USERNAME_HELP_TEXT),
        validators=(UsernameValidator(),),
        error_messages={
            'unique': gettext_lazy(USER_ALREADY_EXIST),
        },
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_NAME, blank=True
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_NAME, blank=True
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER_ROLE
    )
    bio = models.TextField(blank=True)
    # confirmation_code = models.PositiveIntegerField(
    #     blank=True,
    #     validators=[
    #         MinValueValidator(
    #             100000,
    #         ),
    #         MaxValueValidator(
    #             999999,
    #         ),
    #     ])

    @property
    def is_admin_or_superuser(self):
        return (self.role == ADMIN_ROLE or self.is_superuser)

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
