from datetime import date

from django.core.validators import MaxValueValidator


class CurrentYearMaxValueValidator(MaxValueValidator):
    def __init__(self):
        super().__init__(date.today().year)

    def clean(self, x):
        self.limit_value = date.today().year
        return super().clean(x)
