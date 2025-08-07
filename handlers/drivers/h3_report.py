from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from datetime import datetime

from keyboards.reply import reply_report_menu, reply_drive_menu
from services.google_sheets import get_records_by_day, get_records_by_month

router = Router()

MONTHS_RU = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}


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
    telegram_id = message.from_user.id
    today = datetime.now().strftime('%d.%m.%Y')

    records = get_records_by_day(telegram_id, today)

    if not records:
        await message.answer("📅 За сегодня записей не найдено.")
        return

    text_lines = [f"📅 Отчёт за {today}:\n"]
    total_income = total_expense = 0

    for r in records:
        time, rec_type, category, amount, comment = r[1], r[2], r[3], r[4], r[5]
        line = f"{time} • {rec_type.upper()} ({category}) — {amount}₽"
        if comment:
            line += f" — {comment}"
        text_lines.append(line)

        try:
            amt = float(amount.replace(",", "."))
            if rec_type == "доход":
                total_income += amt
            elif rec_type == "расход":
                total_expense += amt
        except ValueError:
            pass

    text_lines.append(f"\nИтого доход: {total_income:.2f}₽")
    text_lines.append(f"Итого расход: {total_expense:.2f}₽")
    text_lines.append(f"Прибыль: {total_income - total_expense:.2f}₽")

    await message.answer("\n".join(text_lines))


@router.message(F.text == "🗓 За месяц")
async def handle_month_report(message: Message):
    """отчёт за текущий месяц"""
    now = datetime.now()
    user_id = message.from_user.id

    records = get_records_by_month(user_id=user_id, month=now.month, year=now.year)

    if not records:
        await message.answer("🗓 За этот месяц записей не найдено.")
        return

    total_income = sum(float(r[4]) for r in records if r[2].lower() == "доход")
    total_expense = sum(float(r[4]) for r in records if r[2].lower() == "расход")

    await message.answer(
        f"🗓 Отчёт за {MONTHS_RU[now.month]} {now.year}:\n"
        f"Доход: {total_income:.2f} ₽\n"
        f"Расход: {total_expense:.2f} ₽\n"
        f"Разница: {total_income - total_expense:.2f} ₽"
    )


@router.message(F.text == "⬅️ Назад")
async def handle_back_to_main(message: Message, state: FSMContext):
    """возврат в главное меню"""
    await state.clear()
    await message.answer(
        "Главное меню:",
        reply_markup=reply_drive_menu()
    )


