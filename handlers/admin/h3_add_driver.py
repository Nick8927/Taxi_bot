from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class AddDriver(StatesGroup):
    """состояния: добавления водителя"""
    waiting_for_id = State()


@router.message(F.text == "➕ Добавить водителя")
async def ask_for_driver_id(message: Message, state: FSMContext):
    """добавление водителя"""
    await state.set_state(AddDriver.waiting_for_id)
    await message.answer("Введите Telegram ID нового водителя:")


@router.message(AddDriver.waiting_for_id)
async def save_driver_id(message: Message, state: FSMContext):
    """сохранение ID водителя"""
    tg_id = message.text.strip()
    # TODO: добавить в Google Sheets
    await message.answer(f"✅ Водитель с ID {tg_id} добавлен.")
    await state.clear()
