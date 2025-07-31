from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import  reply_admin_menu, reply_drive_menu
from utils.auth import is_driver, is_admin

router = Router()

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    """стартовое меню разграничивающее админку и водителей"""

    user_id = message.from_user.id

    if is_admin(user_id):
        await message.answer("🔐 Админ-панель", reply_markup=reply_admin_menu())
    elif is_driver(user_id):
        await message.answer("Добро пожаловать, водитель!", reply_markup=reply_drive_menu())
    else:
        await message.answer("🚫 У вас нет доступа. Обратитесь к администратору.")
