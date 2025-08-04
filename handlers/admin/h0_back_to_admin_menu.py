from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import reply_admin_menu


router = Router()


@router.message(F.text == "⬅️ Назад")
async def handle_admin_back(message: Message, state: FSMContext):
    """кнопка назад в меню администратора"""
    await state.clear()
    await message.answer("Меню администратора:", reply_markup=reply_admin_menu())
