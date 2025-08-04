from aiogram import Router, F
from aiogram.types import Message
from keyboards.reply import reply_report_menu
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text == "📊 Отчёт")
async def handle_report_menu(message: Message, state: FSMContext):
    """ обработка нажатия на кнопку "Отчёт. /
     также сброс FSM """
    await state.clear()
    await message.answer(
        "Выберите период для отчёта:",
        reply_markup=reply_report_menu()
    )
