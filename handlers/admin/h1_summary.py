from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(F.text == "📊 Сводный отчёт")
async def handle_summary_report(message: Message):
    """ отчет для администратора """
    # fake_report - заглушка, далее заменю на gooogle sheets
    fake_report = (
        "📊 Сводный отчёт:\n"
        "👤 Иванов — Доход: 4500₽, Расход: 1200₽\n"
        "👤 Петров — Доход: 3200₽, Расход: 800₽\n"
        "👤 Сидоров — Доход: 6100₽, Расход: 2000₽"
    )
    await message.answer(fake_report)
