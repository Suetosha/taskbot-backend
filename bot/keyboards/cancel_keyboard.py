from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с кнопкой отмены опроса
def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отменить заполнение")]],
        resize_keyboard=True
    )
