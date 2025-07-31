from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import reply_main_menu

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    """реакция на start и вывод базовой клавиатуры"""
    await message.answer(
        "Привет! Выберите действие:",
        reply_markup=reply_main_menu()
    )
