from __future__ import annotations

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task
from .tasks import notify_task_due


# Планирует одноразовое уведомление о задаче через Celery
@receiver(post_save, sender=Task)
def schedule_due_notification(sender, instance: Task, created: bool, **kwargs) -> None:
    if not created:
        return

    if not instance.due_at:
        return

    def schedule_notification() -> None:
        notify_task_due.apply_async(
            kwargs={"task_id": instance.pk},
            eta=instance.due_at,
        )

    transaction.on_commit(schedule_notification)
