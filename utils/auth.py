from config import ADMIN_ID, ALLOWED_DRIVERS

def is_admin(user_id: int) -> bool:
    """проверка админа"""
    return user_id == ADMIN_ID

def is_driver(user_id: int) -> bool:
    """проверка водителей"""
    return user_id in ALLOWED_DRIVERS
