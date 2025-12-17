import asyncio
from aiogram import Bot, Dispatcher

from handlers import start
from handlers import tasks
from services.api import BackendAPI, BackendConfig
from config import get_bot_token, get_settings


async def main() -> None:
    bot = Bot(token=get_bot_token())
    dp = Dispatcher()

    settings = get_settings()

    dp["api"] = BackendAPI(
        BackendConfig(
            base_url=settings["BACKEND_BASE_URL"],
            bot_secret=settings["BOT_API_SECRET"],
        )
    )

    dp.include_router(start.router)
    dp.include_router(tasks.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
