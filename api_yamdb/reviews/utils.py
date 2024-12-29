from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


# class CurrentYearMaxValueValidator(MaxValueValidator):
#     def __init__(self):
#         super().__init__(date.today().year)

#     def clean(self, x):
#         self.limit_value = date.today().year
#         return super().clean(x)


def current_year_max_value_validator(value):
    if value > date.today().year:
        raise ValidationError(f"{value} превышает текущий год.")
