# modules/admin/handlers/ban.py

from aiogram import Router, types
from modules.decorators import admin_only
from ..services.ban import ban_user, unban_user
from modules.ui.keyboards.tracker import send_managed_message
from aiogram.filters import Command

router = Router()

@router.message(Command("ban"))
@admin_only
async def cmd_ban(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        return await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=f"Использование: /ban [user_id] [причина]"
        )
    user_id, reason = parts[1], parts[2]
    try:
        uid = int(user_id)
        ban_user(uid, reason)
        await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=f"Пользователь {user_id} заблокирован по причине:\n<i>{reason}</i>"
        )
    except ValueError:
        await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text="Неверный user_id. Он должен быть числом"
        )

@router.message(Command("unban"))
@admin_only
async def cmd_unban(message: types.Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text="Использование: /unban [user_id]"
        )
    try:
        uid = int(parts[1])
        unban_user(uid)
        await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=f"Пользователь {uid} разблокирован"
        )
    except ValueError:
        await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text="Неверный user_id. Он должен быть числом"
        )