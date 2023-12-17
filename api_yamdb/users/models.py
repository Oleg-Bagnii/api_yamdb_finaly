from django.contrib.auth.models import AbstractUser
from django.db import models

from api.v1.validators import validator


MAX_LENGTH = 150


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
        )
    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LENGTH,
        unique=True,
        validators=(validator,),
        )
    email = models.EmailField(
        'Электронная почта',
        unique=True
        )
    first_name = models.CharField(
        'Имя',
        max_length=MAX_LENGTH,
        blank=True
        )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH,
        blank=True
        )
    bio = models.TextField(
        'Биография',
        blank=True
        )
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=CHOICES,
        default=USER,
        )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[: 30]
