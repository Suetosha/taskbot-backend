from __future__ import annotations

import json
import urllib.request

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Task

# Процесс отправления таски в бот
def _telegram_send_message(chat_id: int, text: str) -> None:
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан в settings")

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=10) as resp:
        body = resp.read().decode("utf-8")
        if resp.status >= 400:
            raise RuntimeError(f"Telegram API ошибка {resp.status}: {body}")


# Проверяет данные и отправляет уведомление пользователю
@shared_task
def notify_task_due(task_id: str) -> str:
    try:
        task = Task.objects.select_related("user").get(pk=task_id)
    except Task.DoesNotExist:
        return "Задача не найдена"

    if task.is_completed:
        return "Задача уже выполнена"

    if not task.due_at:
        return "Не задан срок (due_at)"

    if not task.user.telegram_id:
        return "У пользователя не указан telegram_id"

    chat_id = int(task.user.telegram_id)

    text = (
        "Напоминание о задаче:\n"
        f"{task.title}\n"
        f"{task.description}\n"
        f"Срок: {timezone.localtime(task.due_at).strftime('%d.%m.%Y %H:%M')}"
    )
    _telegram_send_message(chat_id=chat_id, text=text)

    task.is_completed = True
    task.save(update_fields=["is_completed"])

    return "Сообщение отправлено"
