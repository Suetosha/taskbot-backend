from django.db import models
import ulid

class BaseModel(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=26,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = ulid.new().str
        super().save(*args, **kwargs)

    class Meta:
        abstract = True