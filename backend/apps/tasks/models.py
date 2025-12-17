from django.db import models
from ..common.models import BaseModel

class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    categories = models.ManyToManyField(
        "categories.Category",
        related_name="tasks",
        blank=True
    )

    due_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

