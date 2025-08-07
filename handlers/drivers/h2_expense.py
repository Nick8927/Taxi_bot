from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from services.google_sheets import add_record


router = Router()


class ExpenseStates(StatesGroup):
    """ожидание ввода суммы и комментария"""
    waiting_for_amount_and_comment = State()


@router.message(F.text == "💸 Расход")
async def expense_start(message: Message, state: FSMContext):
    """начало ввода расхода"""
    await message.answer(
        "Введите сумму и комментарий (через пробел):\nНапример:\n`150 мойка машины`",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="Markdown"
    )
    await state.set_state(ExpenseStates.waiting_for_amount_and_comment)


@router.message(ExpenseStates.waiting_for_amount_and_comment)
async def expense_received(message: Message, state: FSMContext):
    """получение суммы и комментария"""
    text = message.text.strip()
    parts = text.split(" ", 1)


    try:
        amount = float(parts[0].replace(",", "."))
        comment = parts[1] if len(parts) > 1 else ""

        add_record(
            user_id=message.from_user.id,
            username=message.from_user.full_name,
            record_type='расход',
            subcategory="-",
            amount=amount,
            comment=comment
        )

        await message.answer(f"✅ Расход сохранён:\nСумма: {amount}\nКомментарий: {comment}")
        await state.clear()

    except ValueError:
        await message.answer("❌ Неверный формат. Повторите ввод: `150 мойка машины`")