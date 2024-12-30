from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from reviews.constants import ALREADY_EXIST_FIELD


USERNAME_REGEX = r'^[\w.@+-]+\Z'

USERNAME_VALIDATE_MASSAGE = (
    'Введите действительное имя пользователя. '
    'Это значение может содержать только буквы '
    'числа, и символы: @/./+/-/_ .'
)


def validate_current_year(year):
    if year < date.today().year:
        return year
    raise ValidationError(
        f'Год выпуска ({year}) не может быть позже текущего года.')


def validate_username(username: str):
    RegexValidator(
        regex=USERNAME_REGEX,
        message=USERNAME_VALIDATE_MASSAGE
    )(username)
    if username == settings.USERNAME:
        raise ValidationError(
            {'username': ALREADY_EXIST_FIELD.format(settings.USERNAME)}
        )
