from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.cancel_keyboard import get_cancel_keyboard
from utils.formatters import render_task

from utils.time_utils import datetime_to_iso, parse_user_datetime

router = Router()


class AddTask(StatesGroup):
    title = State()
    description = State()
    due_at = State()
    categories = State()


@router.message(Command("tasks"))
async def cmd_tasks(message: Message, api) -> None:
    telegram_id = message.from_user.id

    categories = await api.list_categories(telegram_id)
    cat_map = {str(c["id"]): c.get("name", str(c["id"])) for c in categories}

    tasks = await api.list_tasks(telegram_id)
    if not tasks:
        await message.answer("У вас пока нет задач")
        return

    text = "Ваши задачи:\n\n" + "\n\n".join(render_task(t, cat_map) for t in tasks)
    await message.answer(text)


@router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext) -> None:
    await state.set_state(AddTask.title)
    await message.answer(
        "Введите заголовок задачи:",
        reply_markup = get_cancel_keyboard()
        )


@router.message(F.text == "Отменить заполнение")
async def btn_cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Заполнение задачи отменено", reply_markup=ReplyKeyboardRemove())


@router.message(AddTask.title, F.text)
async def add_title(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()
    if not title:
        await message.answer("Заголовок не может быть пустым. Введите заголовок:")
        return

    await state.update_data(title=title)
    await state.set_state(AddTask.description)
    await message.answer("Введите описание:")


@router.message(AddTask.description, F.text)
async def add_description(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    description = "" if text == "-" else text

    await state.update_data(description=description)
    await state.set_state(AddTask.due_at)
    await message.answer(
        "Введите срок в формате ДД.ММ.ГГГГ ЧЧ:ММ (например 20.12.2025 18:30)\n"
    )


@router.message(AddTask.due_at, F.text)
async def add_due_at(message: Message, state: FSMContext) -> None:
    try:
        due_at_iso = parse_user_datetime(message.text)

    except ValueError as e:
        await message.answer(str(e))
        return

    await state.update_data(due_at=due_at_iso)
    await state.set_state(AddTask.categories)
    await message.answer("Введите категории через запятую:")


@router.message(AddTask.categories, F.text)
async def add_categories(message: Message, state: FSMContext, api) -> None:
    telegram_id = message.from_user.id
    raw = (message.text or "").strip()

    data = await state.get_data()
    title = data["title"]
    description = data.get("description", "")
    due_at = data.get("due_at")

    try:
        category_ids: list[str] = []
        if raw != "-":
            names = [x.strip() for x in raw.split(",") if x.strip()]
            for name in names:
                c = await api.get_or_create_category_by_name(telegram_id, name)
                category_ids.append(str(c["id"]))

        task = await api.create_task(
            telegram_id=telegram_id,
            title=title,
            description=description,
            category_ids=category_ids,
            due_at=due_at,
        )
    except Exception as e:
        await message.answer(f"Не удалось создать задачу: {e}\nПопробуйте снова: /add")
        await state.clear()
        return

    await state.clear()
    await message.answer(
        "<b>Задача создана!</b>\n\n"
        f"<b>Категория:</b> {raw}\n"
        f"<b>Заголовок:</b> {task.get('title')}\n"
        f"<b>Создано:</b> {datetime_to_iso(task.get('created_at'))}\n"
        f"<b>Срок:</b> {datetime_to_iso(task.get('due_at'))}\n\n"
        "Посмотреть список: /tasks",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='HTML'
    )
