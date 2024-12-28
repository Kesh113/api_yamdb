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
from reviews.utils import CurrentYearMaxValueValidator


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
    name = models.CharField(max_length=256, verbose_name='название')
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_STR_LEN]


class TextAuthorPubdateBaseModel(models.Model):
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(auto_now_add=True)

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
    name = models.CharField(max_length=256, verbose_name='название')
    year = models.PositiveIntegerField(
        validators=[CurrentYearMaxValueValidator()]
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name[:MAX_STR_LEN]


class Review(TextAuthorPubdateBaseModel):
    score = models.PositiveIntegerField(verbose_name='оценка',
        validators=[MaxValueValidator(MAX_SCORE,),
                    MinValueValidator(MIN_SCORE)])
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        null=True
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
        on_delete=models.CASCADE
    )

    class Meta(TextAuthorPubdateBaseModel.Meta):
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
