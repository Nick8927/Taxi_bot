from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton


def inline_pay_button(amount: float, url: str):
    """
    кнопка для оплаты
    """

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳 Оплатить {amount:.0f} ₽", url=url)]
        ]
    )