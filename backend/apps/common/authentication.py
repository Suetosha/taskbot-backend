from __future__ import annotations

import secrets

from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from ..users.models import User


# Аутентификация запросов от телеграм бота, проверяет X-Bot-Secret
class BotTelegramAuthentication(BaseAuthentication):
    def authenticate(self, request):
        expected = getattr(settings, "BOT_API_SECRET", "")
        provided = request.headers.get("X-Bot-Secret")

        if not expected:
            raise AuthenticationFailed("BOT_API_SECRET не настроен на сервере")

        if not provided:
            raise AuthenticationFailed("Отсутствует X-Bot-Secret")

        expected_b = str(expected).encode("utf-8")
        provided_b = str(provided).encode("utf-8")

        if not secrets.compare_digest(provided_b, expected_b):
            raise AuthenticationFailed("Неверный X-Bot-Secret")

        tg_id = request.headers.get("X-Telegram-Id")
        if not tg_id:
            raise AuthenticationFailed("Отсутствует X-Telegram-Id")

        try:
            telegram_id = int(tg_id)
        except ValueError as e:
            raise AuthenticationFailed("X-Telegram-Id должен быть числом") from e

        user, _ = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={"username": f"tg_{telegram_id}"},
        )
        return user, None