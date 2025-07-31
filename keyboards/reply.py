from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_main_menu():
    """базовая клавиатура"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="💰 Доход")
    builder.button(text="💸 Расход")
    builder.button(text="📊 Отчёт")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)
