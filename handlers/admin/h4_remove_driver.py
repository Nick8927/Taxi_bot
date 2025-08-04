from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()


class RemoveDriver(StatesGroup):
    """состояния: удаления водителя"""
    waiting_for_id = State()


@router.message(F.text == "❌ Удалить водителя")
async def ask_for_driver_id_to_remove(message: Message, state: FSMContext):
    """запрос ID водителя для удаления"""
    await state.set_state(RemoveDriver.waiting_for_id)
    await message.answer("Введите Telegram ID водителя, которого нужно удалить:")


@router.message(RemoveDriver.waiting_for_id)
async def remove_driver_id(message: Message, state: FSMContext):
    """удаление водителя по ID"""
    tg_id = message.text.strip()
    # TODO: удалить из Google Sheets или базы
    await message.answer(f"🗑 Водитель с ID {tg_id} удалён.")
    await state.clear()
