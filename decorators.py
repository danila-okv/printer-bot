from functools import wraps
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS

def admin_only(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user_id = None

        # Ищем user_id среди аргументов
        for arg in args:
            if isinstance(arg, (Message, CallbackQuery)):
                user_id = arg.from_user.id
                break

        if user_id not in ADMIN_IDS:
            # Мягко отвечаем, будто такой команды не существует
            if isinstance(arg, Message):
                await arg.answer("🤖 Я не знаю такой команды.")
            elif isinstance(arg, CallbackQuery):
                await arg.answer()  # без текста = молча
            return

        return await func(*args, **kwargs)

    return wrapper