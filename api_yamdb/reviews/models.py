from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxValueValidator,
    RegexValidator, MinValueValidator
)
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy

from api.constants import (
    ADMIN_ROLE, MAX_LENGTH_EMAIL, MAX_LENGTH_FIRST_LAST_NAME,
    MODERATOR_ROLE, USER_ROLE, USERNAME_BAN, MAX_LENGTH_USERNAME,
    MAX_SCORE, MAX_STR_LEN, MIN_SCORE
)
from reviews.utils import current_year_max_value_validate


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
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
        unique=True,
        help_text=gettext_lazy(USERNAME_HELP_TEXT),
        validators=(UsernameValidator(),),
        error_messages={
            'unique': gettext_lazy(USER_ALREADY_EXIST),
        },
        verbose_name='Пользовательское'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_NAME,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH_FIRST_LAST_NAME,
        blank=True,
        verbose_name='Фамилия'
    )
    role = models.CharField(
        max_length=MAX_LENGTH_ROLE,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )

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


class NameSlugBaseModel(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Путь'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_STR_LEN]


class TextAuthorPubdateBaseModel(models.Model):
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        default_related_name = '%(class)ss'

    def __str__(self):
        return self.text[:MAX_STR_LEN]


class Genre(NameSlugBaseModel):
    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Category(NameSlugBaseModel):
    class Meta(NameSlugBaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    year = models.PositiveIntegerField(
        validators=[current_year_max_value_validate()],
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_STR_LEN]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанры'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведения'
    )


class Review(TextAuthorPubdateBaseModel):
    score = models.PositiveIntegerField(
        verbose_name='Оценка',
        validators=[MaxValueValidator(MAX_SCORE,),
                    MinValueValidator(MIN_SCORE)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Произведение'
    )

    class Meta(TextAuthorPubdateBaseModel.Meta):
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_review_per_title'
            ),
        )


class Comment(TextAuthorPubdateBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(TextAuthorPubdateBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
