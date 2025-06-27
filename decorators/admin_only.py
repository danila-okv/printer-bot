from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from config import ADMIN_IDS
from utils.keyboard_tracker import send_managed_message
from messages import ACCESS_DENIED_TEXT

def admin_only(handler):
    @wraps(handler)
    async def wrapper(event, *args, **kwargs):
        user_id = getattr(event.from_user, "id", None)

        if user_id not in ADMIN_IDS:
            try:
                if isinstance(event, Message):
                    await send_managed_message(
                        bot=event.bot,
                        user_id=user_id,
                        text=ACCESS_DENIED_TEXT
                        )
                elif isinstance(event, CallbackQuery):
                    return
            except TelegramBadRequest:
                pass
            return
        return await handler(event, *args, **kwargs)
    return wrapper
