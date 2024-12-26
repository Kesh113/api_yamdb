from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=13, choices=ROLE_CHOICES, default='user'
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.username[:21]}, роль - {self.role}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = 'username',
