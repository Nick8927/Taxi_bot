from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.payments import create_payment
from keyboards.inline import inline_pay_button

router = Router()

@router.message(Command("pay"))
async def cmd_pay(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name or ""
    amount = 100.0
    description = f"Пополнение баланса для {username} ({user_id})"

    try:
        confirmation_url, payment_id = await create_payment(amount, description, user_id, username)
    except Exception as e:
        await message.answer(f"Ошибка создания платежа: {e}")
        return

    kb = inline_pay_button(amount, confirmation_url)

    await message.answer(
        f"Счёт создан. ID платежа: `{payment_id}`\nНажми кнопку для оплаты.",
        reply_markup=kb,
        parse_mode="Markdown"
    )
