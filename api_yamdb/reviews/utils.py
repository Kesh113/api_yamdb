from datetime import date

from django.core.validators import MaxValueValidator


def current_year_max_value_validate():
    return MaxValueValidator(limit_value=date.today().year)
