from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import reply_admin_report_menu, reply_admin_menu
from services.google_sheets import get_admin_summary

router = Router()

@router.message(F.text == "📊 Сводный отчёт")
async def admin_summary_menu(message: Message, state: FSMContext):
    """выбор периода для сводного отчёта"""
    await state.clear()
    await message.answer(
        "Выберите период для сводного отчёта:",
        reply_markup=reply_admin_report_menu()
    )


@router.message(F.text == "📅 Сегодня")
async def admin_summary_today(message: Message):
    """отчёт за сегодня"""
    report = get_admin_summary("day")
    await message.answer(f"📅 Сводный отчёт за сегодня:\n{report}")


@router.message(F.text == "🗓 Этот месяц")
async def admin_summary_month(message: Message):
    """отчёт за месяц"""
    report = get_admin_summary("month")
    await message.answer(f"🗓 Сводный отчёт за месяц:\n{report}")


@router.message(F.text == "♾ Всё время")
async def admin_summary_all(message: Message):
    """отчёт за всё время"""
    report = get_admin_summary("all")
    await message.answer(f"♾ Сводный отчёт за всё время:\n{report}")


@router.message(F.text == "⬅️ Назад")
async def back_to_admin_menu(message: Message, state: FSMContext):
    """возврат в админ-меню"""
    await state.clear()
    await message.answer(
        "Админ-меню:",
        reply_markup=reply_admin_menu()
    )
