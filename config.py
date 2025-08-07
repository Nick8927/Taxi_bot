import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

ALLOWED_DRIVERS = [7213094751, 987654321, 1834794267]

GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDS_PATH", "services/creds/credentials.json")