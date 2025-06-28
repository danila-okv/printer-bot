# modules/admin/bot_control.py

from db import get_connection
from typing import Optional, List, Dict

PAUSE_KEY = 'paused'

def set_pause(reason: str) -> None:
    """Установить флаг паузы с причиной."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO bot_state(key, value) VALUES (?, ?)",
            (PAUSE_KEY, reason)
        )
        conn.commit()

def clear_pause() -> None:
    """Снять флаг паузы."""
    with get_connection() as conn:
        conn.execute("DELETE FROM bot_state WHERE key = ?", (PAUSE_KEY,))
        conn.commit()

def is_paused() -> bool:
    """Проверить, стоит ли флаг паузы."""
    cur = get_connection().execute(
        "SELECT 1 FROM bot_state WHERE key = ?", (PAUSE_KEY,)
    )
    return cur.fetchone() is not None

def get_pause_reason() -> Optional[str]:
    """Получить текст причины паузы."""
    cur = get_connection().execute(
        "SELECT value FROM bot_state WHERE key = ?", (PAUSE_KEY,)
    )
    row = cur.fetchone()
    return row['value'] if row else None

def queue_action(user_id: int, action: str) -> None:
    """Сохранить попытку пользователя сделать что-то во время паузы."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO paused_actions(user_id, action) VALUES (?, ?)",
            (user_id, action)
        )
        conn.commit()

def pop_all_queued_actions() -> List[Dict]:
    """
    Вытянуть и удалить из очереди все отложенные действия.
    Возвращает список dict-ов с полями id, user_id, action.
    """
    with get_connection() as conn:
        cur = conn.execute(
            "SELECT id, user_id, action FROM paused_actions ORDER BY created_at"
        )
        rows = [dict(row) for row in cur.fetchall()]
        conn.execute("DELETE FROM paused_actions;")
        conn.commit()
    return rows

from functools import wraps
from aiogram import types

from functools import wraps
from aiogram import types
from db import get_connection

# — ваш код по флагам is_paused(), queue_action() и т.п. —

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
