from datetime import date

from django.core.exceptions import ValidationError


def validate_current_year(year):
    if year > date.today().year:
        raise ValidationError(
            f'Год выпуска ({year}) не может быть позже текущего года.')
