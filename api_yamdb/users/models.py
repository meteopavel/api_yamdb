from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """
    Кастомная модель пользователя MyUser.

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

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    role = models.CharField('Роль', max_length=20, blank=True)
    bio = models.TextField('Биография', blank=True)
    email = models.EmailField('Электронная почта', unique=True)

    @property
    def is_admin(self):
        """
        Проверка пользователя на наличие прав администратора.

        Администратор имеет полные права на управление всем контентом проекта.
        Может создавать и удалять произведения, категории и жанры,
        а также назначать роли другим пользователям.
        """
        return self.role in [self.ADMIN, self.is_superuser]

    @property
    def is_moderator(self):
        """
        Проверка пользователя на наличие прав модератора.

        Модератор имеет все права аутентифицированного пользователя и,
        дополнительно, право удалять и редактировать любые отзывы и коммент.
        """
        return self.role in [self.MODERATOR, self.ADMIN, self.is_superuser]

    @property
    def is_user(self):
        """Проверка пользователя на наличие стандартных прав."""
        return self.role in [self.USER]

    class Meta:
        """
        Дополнительные настройки.

        Атрибуты:
        - constraints: Ограничения - уникальное сочетание полей.
        - verbose_name: Название модели в единственном числе.
        - verbose_name_plural: Название модели во множественном числе.
        - ordering: Порядок сортировки записей модели.
        """

        constraints = [
            models.UniqueConstraint(fields=('username', 'email'),
                                    name='unique_username_email')
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )
