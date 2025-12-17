import os

import dotenv

dotenv.load_dotenv()


def get_bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Не задана переменная окружения TELEGRAM_BOT_TOKEN")
    return token


def get_settings() -> dict[str, str]:
    base_url = os.getenv("BACKEND_BASE_URL")

    if not base_url:
        raise RuntimeError("BACKEND_BASE_URL не установлен")

    return {
        "BACKEND_BASE_URL": base_url.rstrip("/"),
        "BOT_API_SECRET": os.getenv("BOT_API_SECRET"),
    }
