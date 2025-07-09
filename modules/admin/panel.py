from aiogram import Router, types
from modules.decorators import admin_only
from modules.users.banlist import ban_user, unban_user
from modules.ui.keyboards.tracker import send_managed_message
from aiogram.filters import Command
from modules.admin.bot_control import (
    set_pause, clear_pause,
    pop_all_queued_actions
)

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

@router.message(Command("pause"))
@admin_only
async def cmd_pause(message: types.Message):
    # извлекаем причину (всё, что после команды)
    reason = message.text.partition(' ')[2].strip() or "🤖 Технические работы"
    set_pause(reason)
    await message.reply(f"⏸️ Бот поставлен на пауза.\nПричина: <i>{reason}</i>")

@router.message(Command("resume"))
@admin_only
async def cmd_resume(message: types.Message):
    clear_pause()
    await message.reply("▶️ Бот возобновил работу.")

    # Вытягиваем все отложенные действия и сразу удаляем их из БД
    actions = pop_all_queued_actions()

    # Собираем уникальные user_id
    user_ids = {act['user_id'] for act in actions}

    # Шлём одному разу на каждого
    for uid in user_ids:
        await send_managed_message(
            message.bot,
            uid,
            text="✅ Бот снова в деле!\nСпасибо за терпение - дарю тебе 5 бесплатных страниц 🎉"
        )