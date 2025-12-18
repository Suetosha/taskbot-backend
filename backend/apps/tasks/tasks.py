from __future__ import annotations

import requests

from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import Task

# Процесс отправления таски в бот
def _telegram_send_message(chat_id: int, text: str) -> None:
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}"

    try:
        response = requests.post(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Telegram API ошибка: {e}")


# Проверяет данные и отправляет уведомление пользователю
@shared_task
def notify_task_due(task_id: int) -> str:
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
    categories = task.categories.all()
    categories_text = ", ".join(c.name for c in categories)

    text = (
        "Напоминание о задаче:\n\n"
        f"Название: {task.title}\n"
        f"Описание: {task.description}\n"
        f"Категории: {categories_text}\n"
        f"Срок: {timezone.localtime(task.due_at).strftime('%d.%m.%Y %H:%M')}"
    )
    try:
        _telegram_send_message(chat_id=chat_id, text=text)
    except Exception as e:
        return f"Ошибка отправки: {str(e)}"

    task.is_completed = True
    task.save(update_fields=["is_completed"])

    return "Сообщение отправлено"
