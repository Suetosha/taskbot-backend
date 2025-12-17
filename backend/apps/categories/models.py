from django.db import models

from ..common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(
    max_length=64,
    verbose_name='Название'
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name='Пользователь'
    )

    class Meta:
        unique_together = ("name", "user")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
