from django.contrib.auth.models import AbstractUser
from django.db import models

from ..common.models import BaseModel


class User(BaseModel, AbstractUser):
    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username