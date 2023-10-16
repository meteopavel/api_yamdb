from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя User.

    Поля:
    - role: Роль пользователя (Пользователь, Модератор, Администратор).
    - bio: Биография пользователя.
    - email: Адрес электронной почты пользователя.

    Свойства:
    - is_admin: Возвращает True, если пользователь имеет роль администратора
    или является суперпользователем.
    - is_moderator: Возвращает True, если пользователь имеет роль модератора.

    Роли определены в кортеже ROLES.
    """

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.MAX_STRING_LENGTH_254,
        unique=True
    )

    @property
    def is_admin(self):
        """
        Проверка пользователя на наличие прав администратора.

        Администратор имеет полные права на управление всем контентом проекта.
        Может создавать и удалять произведения, категории и жанры,
        а также назначать роли другим пользователям.
        """
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        """
        Проверка пользователя на наличие прав модератора.

        Модератор имеет все права аутентифицированного пользователя и,
        дополнительно, право удалять и редактировать любые отзывы и коммент.
        """
        return self.role == self.MODERATOR
    
    @property
    def is_admin_or_superuser_or_staff(self):
        return self.role in (User.ADMIN, User.MODERATOR, User.STAFF)

    class Meta:
        """
        Дополнительные настройки.

        Атрибуты:
        - constraints: Ограничения - уникальное сочетание полей.
        - verbose_name: Название модели в единственном числе.
        - verbose_name_plural: Название модели во множественном числе.
        - ordering: Порядок сортировки записей модели.
        """

        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
