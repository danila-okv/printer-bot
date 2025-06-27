import sqlite3
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup

DB_PATH = "data/bot.db"

def get_active_message_id(user_id: int) -> int | None:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT message_id FROM active_keyboards WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else None

def update_active_message(user_id: int, message_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO active_keyboards (user_id, message_id)
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET message_id = excluded.message_id
        """, (user_id, message_id))
        conn.commit()

async def send_managed_message(
    bot: Bot,
    user_id: int,
    text: str,
    reply_markup: InlineKeyboardMarkup | None = None,
    parse_mode: str = "HTML"
) -> Message:
    old_msg_id = get_active_message_id(user_id)

    if old_msg_id:
        try:
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=old_msg_id, reply_markup=None)
        except Exception:
            pass

    # Отправляем новое сообщение
    new_msg = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)

    # Сохраняем новое как активное
    update_active_message(user_id, new_msg.message_id)
    return new_msg
