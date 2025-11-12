import os
import uuid
import aiohttp
from typing import  Dict

YOOKASSA_API = "https://api.yookassa.ru/v3"
SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")
RETURN_URL = os.getenv("YOOKASSA_RETURN_URL", "")

pending_payments: Dict[str, dict] = {}


async def create_payment(amount: float, description: str, user_id: int, username: str):
    """
    Создаёт платёж в YooKassa и возвращает (confirmation_url, payment_id).
    Также создаёт запись в  (pending) для GS нужно написать webhook .
    """
    idempotence_key = str(uuid.uuid4())
    payload = {
        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": RETURN_URL},
        "capture": True,
        "description": description
    }
    auth = aiohttp.BasicAuth(login=SHOP_ID, password=SECRET_KEY)

    async with aiohttp.ClientSession(auth=auth) as session:
        headers = {"Idempotence-Key": idempotence_key, "Accept": "application/json"}
        async with session.post(f"{YOOKASSA_API}/payments", json=payload, headers=headers) as resp:
            data = await resp.json()
            print(f"create_payment response: {resp.status} {data}")

            if resp.status not in (200, 201):
                raise RuntimeError(f"YooKassa create payment failed: {resp.status} {data}")

            payment_id = data.get("id")
            confirmation = data.get("confirmation", {})
            confirmation_url = confirmation.get("confirmation_url") or confirmation.get("url") or ""

            pending_payments[payment_id] = {
                "user_id": user_id,
                "username": username or "",
                "amount": amount,
                "status": "pending"
            }

            try:
                from services.google_sheets import add_record
                comment = f"payment_created:{payment_id}"
                add_record("income", "yookassa_pending", amount, comment, user_id, username or "")
            except Exception as e:
                print(f"add_record failed on payment creation: {e}")

            return confirmation_url, payment_id


async def get_payment_status(payment_id: str) :
    """
    Запрашивает статус платежа у YooKassa. Фича не работает без webhook
    """
    auth = aiohttp.BasicAuth(login=SHOP_ID, password=SECRET_KEY)
    async with aiohttp.ClientSession(auth=auth) as session:
        async with session.get(f"{YOOKASSA_API}/payments/{payment_id}") as resp:
            if resp.status != 200:
                try:
                    text = await resp.text()
                    print(f"get_payment_status failed {resp.status} {text}")
                except Exception:
                    print(f"get_payment_status failed {resp.status}")
                return None
            data = await resp.json()
            print(f"get_payment_status response: {payment_id} {data.get('status')}")
            return data


async def mark_payment_record(payment_id: str, status: str):
    """
    Фича не работает без webhook
    Обновляет локальную память и добавляет/обновляет запись в Google Sheets.
    При status == 'succeeded' — записывает фактическую оплату.

    """
    info = pending_payments.get(payment_id, {})
    user_id = info.get("user_id")
    username = info.get("username", "")
    amount = info.get("amount", 0.0)

    if info:
        info["status"] = status

    try:
        from services.google_sheets import add_record
        comment = f"payment_id:{payment_id} status:{status}"
        if status == "succeeded":
            add_record("income", "yookassa", amount, comment, user_id, username or "")
        else:
            add_record("income", "yookassa_update", 0.0, comment, user_id, username or "")
        print(f"mark_payment_record: {payment_id} status {status}")
    except Exception as e:
        print(f"add_record failed on payment update: {e}")
