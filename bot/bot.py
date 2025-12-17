import asyncio
from aiogram import Bot, Dispatcher

from config import get_bot_token
from handlers import routers


async def main() -> None:
    bot = Bot(token=get_bot_token())
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())