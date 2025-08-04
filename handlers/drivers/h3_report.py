from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import reply_report_menu, reply_drive_menu

router = Router()

@router.message(F.text == "📊 Отчёт")
async def handle_report_menu(message: Message, state: FSMContext):
    """обработка нажатия на кнопку "Отчёт. /
         также сброс FSM"""
    await state.clear()
    await message.answer(
        "Выберите период для отчёта:",
        reply_markup=reply_report_menu()
    )


@router.message(F.text == "📅 Текущий день")
async def handle_today_report(message: Message):
    """отчет за текущий день"""
    # TODO: позже добавлю Google Sheets
    await message.answer("📅 Отчёт за текущий день:\n(данные появятся позже)")


@router.message(F.text == "🗓 За месяц")
async def handle_month_report(message: Message):
    """отчет за месяц"""
    # TODO: позже добавлю Google Sheets
    await message.answer("🗓 Отчёт за месяц:\n(данные появятся позже)")


@router.message(F.text == "⬅️ Назад")
async def handle_back_to_main(message: Message, state: FSMContext):
    """возврат в главное меню"""
    await state.clear()
    await message.answer(
        "Главное меню:",
        reply_markup=reply_drive_menu()
    )


