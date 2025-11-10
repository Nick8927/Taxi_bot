from aiogram import Router, types, F
import json
from services.google_sheets import add_record

router = Router()

@router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Обработка данных из мини-аппа"""

    web_data = message.web_app_data
    if not web_data or not web_data.data:
        await message.answer("Нет данных от мини-аппа.")
        return

    try:
        data = json.loads(web_data.data)
    except json.JSONDecodeError:
        await message.answer("Неверный формат данных.")
        return

    record_type = str(data.get("record_type", "доход"))
    subcategory = str(data.get("subcategory", "webapp"))

    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        await message.answer("Некорректная сумма.")
        return

    comment = str(data.get("comment", "-"))

    try:
        add_record(
            record_type=record_type,
            subcategory=subcategory,
            amount=amount,
            comment=comment,
            user_id=message.from_user.id,
            username=message.from_user.full_name
        )

        await message.answer(
            f"✅ Запись добавлена:\n"
            f"Тип: {record_type}\n"
            f"Подкатегория: {subcategory}\n"
            f"Сумма: {amount:.2f} ₽\n"
            f"Комментарий: {comment}"
        )
    except Exception as e:
        await message.answer(f"Ошибка при записи в Google Sheets: {e}")
