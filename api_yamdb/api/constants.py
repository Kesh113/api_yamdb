USERNAME_BAN = 'me'

ADMIN_ROLE = 'admin'
USER_ROLE = 'user'
MODERATOR_ROLE = 'moderator'

MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_FIRST_LAST_NAME = 150

SUBJECT = 'Код подтверждения'
MESSAGE = 'Ваш код подтверждения: {}'

INVALID_CONFIRM_CODE = 'Неверный код подтверждения'

ONLY_ONE_REVIEW = 'Можно оставить только один отзыв на произведение'

PARAMETRS = [
    {'genre__slug': 'genre'},
    {'category__slug': 'category'},
    {'name': 'name'},
    {'year': 'year'}
]
