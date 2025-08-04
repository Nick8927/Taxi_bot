from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📥 Выгрузка")
async def handle_export_request(message: Message):
    """реакция на команду выгрузки"""
    # TODO: реализовать выгрузку данных из google sheets
    await message.answer("🔄 Позже...  можно будет получить Excel или PDF файл.")


