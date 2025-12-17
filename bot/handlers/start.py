from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Привет! Я ToDo бот.\n"
        "Доступные команды:\n"
        "/tasks — мои задачи\n"
        "/add — добавить задачу\n"
    )