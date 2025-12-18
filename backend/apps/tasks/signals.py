from __future__ import annotations

import logging
from celery.result import AsyncResult
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Task
from .tasks import notify_task_due
from taskbot_backend.celery import app

logger = logging.getLogger(__name__)

# Планирует одноразовое уведомление о задаче через celery
@receiver(post_save, sender=Task)
def schedule_due_notification(
    sender,
    instance: Task,
    created: bool,
    update_fields=None,
    **kwargs,
) -> None:

    if instance.is_completed:
        return

    # Обработка обновления задачи только при изменении срока (due_at)
    if not created and update_fields and "due_at" not in update_fields:
        return

    if not instance.due_at:
        Task.objects.filter(pk=instance.pk).update(celery_task_id=None)
        return

    def schedule_notification() -> None:
        # Отмена старой таски
        if instance.celery_task_id:
            AsyncResult(instance.celery_task_id).revoke()

        # Планирование новой таски
        if instance.due_at > timezone.now():
            result = notify_task_due.apply_async(
                args=(instance.pk,),
                eta=instance.due_at,
            )

            Task.objects.filter(pk=instance.pk).update(
                celery_task_id=result.id
            )
        else:
            Task.objects.filter(pk=instance.pk).update(celery_task_id=None)

    transaction.on_commit(schedule_notification)

