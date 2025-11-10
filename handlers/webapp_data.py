from aiogram import Router, types
import json
from services.google_sheets import add_record

router = Router()


@router.message(content_types=['web_app_data'])
async def handle_webapp_data(message: types.Message):
    """Обработка данных из мини-аппа"""
    try:
        data = json.loads(message.web_app_data.data)
        record_type = data.get("record_type")
        subcategory = data.get("subcategory")
        amount = float(data.get("amount", 0))
        comment = data.get("comment", "")

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
        await message.answer(f"Ошибка при обработке данных: {e}")
