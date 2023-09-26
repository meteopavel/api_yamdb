from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    role = models.TextField('Роль', blank=True)
    bio = models.TextField('Биография', blank=True)
