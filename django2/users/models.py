from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя с ролями."""

    ROLE_CHOICES = [
        ('client', 'Клиент'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='client',
        verbose_name='Роль',
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
        blank=True,
        default='',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.username

    @property
    def is_admin_role(self):
        return self.role == 'admin'

    @property
    def is_manager_role(self):
        return self.role == 'manager'

    @property
    def is_client_role(self):
        return self.role == 'client'
