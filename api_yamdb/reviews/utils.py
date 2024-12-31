from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


USERNAME_REGEX = r'^[\w.@+-]+\Z'

USERNAME_VALIDATE_MESSAGE = (
    'Введите действительное имя пользователя. '
    'Это значение может содержать только буквы '
    'числа, и символы: @/./+/-/_ .'
)

FORBIDDEN_USE = 'Использовать имя "{}" в качестве username запрещено.'


def validate_current_year(year):
    if year < date.today().year:
        return year
    raise ValidationError(
        f'Год выпуска ({year}) не может быть позже '
        f'текущего года({date.today().year}).'
    )


def validate_username(username: str):
    RegexValidator(
        regex=USERNAME_REGEX,
        message=USERNAME_VALIDATE_MESSAGE
    )(username)
    if username == settings.USERNAME_RESERVED:
        raise ValidationError(
            {'username': FORBIDDEN_USE.format(settings.USERNAME_RESERVED)}
        )
    return username
