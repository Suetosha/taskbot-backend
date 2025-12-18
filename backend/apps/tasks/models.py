from django.db import models
from ..common.models import BaseModel


class Task(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание"
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Пользователь"
    )

    categories = models.ManyToManyField(
        "categories.Category",
        related_name="tasks",
        blank=True,
        verbose_name="Категории"
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Срок"
    )

    celery_task_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        default=None
        )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Выполнено"
        )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.title
