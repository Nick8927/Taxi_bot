from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import income_menu
from services.google_sheets import add_record


router = Router()


class IncomeStates(StatesGroup):
    """выбор типа дохода"""
    choosing_type = State()
    waiting_for_amount = State()
    waiting_for_comment = State()


@router.message(F.text == "💰 Доход")
async def show_income_menu(message: Message, state: FSMContext):
    """показ меню для регистрации дохода"""
    await message.answer("Выберите тип дохода:", reply_markup=income_menu())
    await state.set_state(IncomeStates.choosing_type)


@router.message(IncomeStates.choosing_type, F.text.in_(["Оплата за заказ", "Доплата по заказу"]))
async def ask_income_amount(message: Message, state: FSMContext):
    """запрос суммы дохода"""
    await state.update_data(income_type=message.text)
    await message.answer("Введите сумму:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(IncomeStates.waiting_for_amount)


@router.message(IncomeStates.waiting_for_amount)
async def ask_income_comment(message: Message, state: FSMContext):
    """запрос комментария"""
    try:
        amount = float(message.text.replace(",", "."))
    except ValueError:
        await message.answer("Пожалуйста, введите корректную сумму.")
        return

    await state.update_data(amount=amount)
    await message.answer("Добавьте комментарий (например, адрес, заказ № и т.д.):")
    await state.set_state(IncomeStates.waiting_for_comment)


@router.message(IncomeStates.waiting_for_comment)
async def confirm_income(message: Message, state: FSMContext):
    """подтверждение дохода"""
    user_data = await state.get_data()
    comment = message.text

    income_type = user_data['income_type']
    amount = user_data['amount']

    if income_type == "Оплата за заказ":
        subcategory = "оплата"
    else:
        subcategory = "доплата"

    add_record(
        user_id=message.from_user.id,
        username=message.from_user.full_name,
        record_type='доход',
        subcategory=subcategory,
        amount=amount,
        comment=comment
    )

    await message.answer(
        f"✅ Доход зарегистрирован:\n"
        f"Тип: {income_type}\n"
        f"Сумма: {amount:.2f} ₽\n"
        f"Комментарий: {comment}"
    )
    await state.clear()
