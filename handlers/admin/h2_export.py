import pandas as pd
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from datetime import datetime
from services.google_sheets import get_all_data
from keyboards.reply import reply_export_period_keyboard

router = Router()

@router.message(F.text == "📥 Выгрузка")
async def handle_export_request(message: Message):
    """меню выбора периода для выгрузки"""
    await message.answer("Выберите период для выгрузки данных:", reply_markup=reply_export_period_keyboard())


@router.message(F.text.in_(["📅 За день", "🗓 За месяц", "♾ За всё время"]))
async def handle_export_period(message: Message):
    """выгрузка Excel по выбранному периоду с разделением по пользователям"""
    all_data = get_all_data()

    columns = [col.strip().lower() for col in all_data[0]]
    df = pd.DataFrame(all_data[1:], columns=columns)

    now = datetime.now()
    period_text = message.text

    if period_text == "📅 За день":
        df = df[df['дата'] == now.strftime("%d.%m.%Y")]
        file_name = f"export_day_{now.strftime('%Y-%m-%d')}.xlsx"

    elif period_text == "🗓 За месяц":
        month_year = now.strftime("%m.%Y")
        df = df[df['дата'].str.endswith(month_year)]
        file_name = f"export_month_{now.strftime('%Y-%m')}.xlsx"

    else:
        file_name = f"export_all_{now.strftime('%Y-%m-%d')}.xlsx"

    if df.empty:
        await message.answer("⚠️ Нет данных за выбранный период.")
        return

    with pd.ExcelWriter(file_name, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Все записи", index=False)

        for user, user_df in df.groupby("имя"):
            user_df.to_excel(writer, sheet_name=str(user)[:31], index=False)

        summary = (
            df.groupby("имя")["сумма"]
            .apply(lambda x: pd.to_numeric(x, errors='coerce').sum())
            .reset_index()
        )
        summary.rename(columns={"сумма": "Итого"}, inplace=True)
        summary.to_excel(writer, sheet_name="Сводка", index=False)

    await message.answer_document(
        FSInputFile(file_name),
        caption=f"Выгрузка: {period_text}"
    )
