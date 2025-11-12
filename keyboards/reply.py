from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def reply_drive_menu():
    """Клавиатура для водителя с учетом мини-приложения"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="💰 Доход")
    builder.button(text="💸 Расход")

    webapp_url = "https://programme-kurt-surgeon-argued.trycloudflare.com/index.html"

    builder.button(
        text="🧾 Внести через форму",
        web_app=WebAppInfo(url=webapp_url)
    )

    builder.button(text="📊 Отчёт")
    builder.adjust(1, 1, 1, 1)
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


def reply_income_menu():
    """клавиатура для оплаты заказа"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Оплата за заказ")
    builder.button(text="Доплата по заказу")
    builder.button(text="⬅ Назад")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def reply_report_menu():
    """клавиатура для отчёта водителя"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📅 Текущий день")
    builder.button(text="🗓 За месяц")
    builder.button(text="⬅ Назад")
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


def reply_export_period_keyboard():
    """клавиатура выбора периода для выгрузки (админ)"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 За день")],
            [KeyboardButton(text="🗓 За месяц")],
            [KeyboardButton(text="♾ За всё время")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )


def back_button_kb():
    """клавиатура для шага назад"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="Назад ⬅")
    return builder.as_markup(resize_keyboard=True)


def inline_pay_button(amount: float, url: str):
    """
    Возвращает InlineKeyboardMarkup с одной кнопкой оплаты.
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Оплатить {amount:.0f} ₽", url=url)]
        ]
    )