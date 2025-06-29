from functools import wraps
from aiogram import types
from db import get_connection

from config import ADMIN_IDS
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from modules.ui.messages import ACCESS_DENIED_TEXT
from modules.ui.main_menu import send_main_menu
from modules.ui.keyboard_tracker import send_managed_message
from modules.analytics.logger import warning
def check_paused(func):
    """
    Обёртка для хендлеров:
    если бот на паузе, сохраняет запрос и отвечает юзеру.
    Работает и для Message, и для CallbackQuery.
    """
    @wraps(func)
    async def wrapper(event, *args, **kwargs):
        from modules.admin.bot_control import is_paused, get_pause_reason, queue_action

        if is_paused():
            # определяем user_id
            user_id = event.from_user.id

            # определяем текст действия
            if isinstance(event, types.Message):
                action_text = event.text or "<no text>"
            elif isinstance(event, types.CallbackQuery):
                action_text = event.data or "<no data>"
            else:
                action_text = "<unknown action>"

            # кладём в очередь
            queue_action(user_id, action_text)

            # причина паузы
            reason = get_pause_reason() or "Причина не указана"

            # отвечаем пользователю
            if isinstance(event, types.Message):
                await event.reply(
                    f"🚧 Бот приостановлен: «{reason}»\n"
                    "Ваш запрос сохранён — как только я возобновлю работу, напомню вам об этом."
                )
            else:  # CallbackQuery
                # просто показываем уведомление, не бросаем ошибку
                await event.answer(
                    f"🚧 Бот приостановлен: «{reason}»\n"
                    "Ваш запрос сохранён — напомню вам, когда возобновим работу.",
                    show_alert=True
                )
            return  # не передаём управление в реальный хендлер

        # если не на паузе — передаём дальше
        return await func(event, *args, **kwargs)

    return wrapper


REQUIRED_PRINT_FIELDS = ("file_name", "file_path", "page_count", "price")

def ensure_data(func):
    @wraps(func)
    async def wrapper(update, state: FSMContext, *args, **kwargs):
        # определяем, что это — CallbackQuery или Message
        if isinstance(update, CallbackQuery):
            user_id = update.from_user.id
            send_fn = update.message.answer
            bot = update.bot
        else:
            user_id = update.from_user.id
            send_fn = update.answer
            bot = update.bot

        data = await state.get_data()
        if not all(data.get(k) for k in REQUIRED_PRINT_FIELDS):
            await send_fn("❌ Данные утеряны. Начни сначала.")
            await state.clear()
            await send_main_menu(bot, user_id)
            warning(
                user_id=user_id,
                handler=f"ensure_data:{func.__name__}",
                msg="Data lost"
            )
            return
        # прокидываем data дальше в хендлер
        return await func(update, state, data, *args, **kwargs)

    return wrapper

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
