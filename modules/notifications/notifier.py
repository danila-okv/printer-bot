from aiogram import Bot
from modules.ui.keyboards import print_done_kb
from modules.ui.messages import PRINT_DONE_TEXT
from modules.analytics.logger import info, error

async def notify_print_complete(user_id: int, bot: Bot, file_name: str):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=PRINT_DONE_TEXT.format(file_name=file_name),
            reply_markup=print_done_kb
        )
        info(
            user_id,
            "notifier",
            f"User notified about print completion: {file_name}"
        )
    except Exception as e:
        info(
            user_id,
            "notifier",
            f"Error notifying user about print completion: {e}"
        )