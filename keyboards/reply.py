from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_drive_menu():
    """клавиатура для водителя"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="💰 Доход")
    builder.button(text="💸 Расход")
    builder.button(text="📊 Отчёт")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def reply_admin_menu():
    """админская клавиатура"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Сводный отчёт")
    builder.button(text="📥 Выгрузка")
    builder.button(text="➕ Добавить водителя")
    builder.button(text="❌ Удалить водителя")
    builder.button(text="⬅️ Назад")
    builder.adjust(1, 1, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def income_menu():
    """клавиатура для оплаты заказа"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Оплата за заказ")
    builder.button(text="Доплата по заказу")
    builder.adjust(1, 1)
    return builder.as_markup(resize_keyboard=True)


def reply_report_menu():
    """клавиатура для отчёта водителя"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📅 Текущий день")
    builder.button(text="🗓 За месяц")
    builder.button(text="⬅️ Назад")
    builder.adjust(1, 1, 1)
    return builder.as_markup(resize_keyboard=True)


def reply_admin_report_menu():
    """клавиатура для отчёта админа за определённый период"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Сегодня")],
            [KeyboardButton(text="🗓 Этот месяц")],
            [KeyboardButton(text="♾ Всё время")],
            [KeyboardButton(text="⬅️ Назад")],
        ],
        resize_keyboard=True
    )