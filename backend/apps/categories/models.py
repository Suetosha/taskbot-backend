from django.db import models

from ..common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=64)

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="categories"
    )

    class Meta:
        unique_together = ("name", "user")

    def __str__(self):
        return self.name
