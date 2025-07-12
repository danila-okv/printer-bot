# modules/admin/handlers/control.py

from aiogram import Router, types
from modules.decorators import admin_only
from modules.ui.keyboards.tracker import send_managed_message
from aiogram.filters import Command
from ..services.control import (
    set_pause, clear_pause,
    pop_all_queued_actions
)

router = Router()

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
