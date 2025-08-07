import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import GOOGLE_CREDENTIALS_PATH

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

with open(GOOGLE_CREDENTIALS_PATH, 'r') as f:
    creds_dict = json.load(f)

credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

SPREADSHEET_NAME = "TaxiBot"

spreadsheet = client.open(SPREADSHEET_NAME)
sheet = spreadsheet.sheet1


def add_record(record_type: str, subcategory: str, amount: float, comment: str, user_id: int, username: str):
    """Добавление записи в таблицу, согласно полям в таблице"""

    now = datetime.now()
    row = [
        now.strftime('%d.%m.%Y'),
        now.strftime('%H:%M:%S'),
        record_type,
        subcategory,
        amount,
        comment,
        user_id,
        username
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")


def get_records_by_day(user_id: int, date: str):
    """Получение всех записей по user_id за конкретную дату"""
    rows = sheet.get_all_values()[1:]
    filtered = []

    for row in rows:
        row_date = row[0]
        row_user_id = row[6]
        if row_date == date and str(user_id) == row_user_id:
            filtered.append(row)

    return filtered


def get_records_by_month(user_id: int, month: int, year: int):
    """Получение всех записей по user_id за указанный месяц и год"""
    rows = sheet.get_all_values()[1:]
    filtered = []

    for row in rows:
        try:
            row_date = datetime.strptime(row[0], "%d.%m.%Y")
            row_user_id = row[6]
            if row_date.month == month and row_date.year == year and str(user_id) == row_user_id:
                filtered.append(row)
        except (ValueError, IndexError):
            continue

    return filtered
