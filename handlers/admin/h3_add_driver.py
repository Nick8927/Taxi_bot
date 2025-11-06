from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.reply import reply_admin_menu
from services.google_sheets import add_record

router = Router()


class AddDriver(StatesGroup):
    """состояния: добавления водителя"""
    waiting_for_id = State()
    waiting_for_name = State()


@router.message(F.text == "➕ Добавить водителя")
async def ask_for_driver_id(message: Message, state: FSMContext):
    """добавление водителя"""
    await state.set_state(AddDriver.waiting_for_id)
    await message.answer("Введите Telegram ID нового водителя:")


@router.message(AddDriver.waiting_for_id)
async def receive_driver_id(message: Message, state: FSMContext):
    """Получение ID нового водителя"""
    try:
        new_driver_id = int(message.text)
    except ValueError:
        await message.answer("❌ Введите корректный числовой Telegram ID.")
        return

    await state.update_data(new_driver_id=new_driver_id)
    await state.set_state(AddDriver.waiting_for_name)
    await message.answer("Введите имя водителя:")


@router.message(AddDriver.waiting_for_name)
async def receive_driver_name(message: Message, state: FSMContext):
    """Получение имени нового водителя и запись в Google Sheets"""
    user_data = await state.get_data()
    new_driver_id = user_data['new_driver_id']
    new_driver_name = message.text

    add_record(
        user_id=new_driver_id,
        username=new_driver_name,
        record_type="водитель",
        subcategory="регистрация",
        amount=0,
        comment="Новый водитель добавлен администратором"
    )

    await message.answer(
        f"✅ Новый водитель зарегистрирован:\nID: {new_driver_id}\nИмя: {new_driver_name}",
        reply_markup=reply_admin_menu()
    )
    await state.clear()
