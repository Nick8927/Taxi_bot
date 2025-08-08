from aiogram import Router, F
from aiogram.types import Message

from services.google_sheets import get_full_report

router = Router()

@router.message(F.text == "📊 Сводный отчёт")
async def handle_summary_report(message: Message):
    """отчёт для администратора"""
    report = get_full_report()

    total = report["total"]
    text = (
        f"📊 Сводный отчёт за всё время:\n"
        f"Доход: {total['income']:.2f} ₽\n"
        f"Расход: {total['expense']:.2f} ₽\n"
        f"Разница: {total['diff']:.2f} ₽\n\n"
        f"👤 По пользователям:\n"
    )

    for username, stats in report["users"].items():
        text += (
            f"{username} — Доход: {stats['income']:.2f} ₽\n "
            f"Расход: {stats['expense']:.2f} ₽\n "
            f"Разница: {stats['diff']:.2f} ₽\n"
        )

    await message.answer(text)
