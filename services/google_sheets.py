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


def add_record(record_type: str, category: str, amount: float, comment: str, telegram_id: int, name: str):
    """Добавление записи в таблицу, согласно полям в таблице"""

    now = datetime.now()
    row = [
        now.strftime('%d.%m.%Y'),
        now.strftime('%H:%M:%S'),
        record_type,
        category,
        amount,
        comment,
        telegram_id,
        name
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")
