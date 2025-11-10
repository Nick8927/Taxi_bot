from aiogram import Router, types, F
import json
from services.google_sheets import add_record

router = Router()


@router.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    """Обработка данных из мини-аппа"""
    if not message.web_app_data or not message.web_app_data.data:
        await message.answer("❌ Нет данных от мини-аппа.")
        return

    try:
        data = json.loads(message.web_app_data.data)
    except json.JSONDecodeError:
        await message.answer("❌ Неверный формат данных.")
        return


    record_type = data.get("record_type", "доход")
    subcategory = data.get("subcategory", "webapp")
    amount = float(data.get("amount", 0))
    comment = data.get("msg", data.get("comment", "-"))

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
