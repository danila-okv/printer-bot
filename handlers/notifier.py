from aiogram import Bot
from keyboards import print_done_keyboard
from messages import PRINT_DONE_TEXT
from logger import log

async def notify_print_complete(user_id: int, bot: Bot, file_name: str):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=PRINT_DONE_TEXT.format(file_name=file_name),
            reply_markup=print_done_keyboard
        )
        log(user_id, "notify_print_complete", f"User notified about print completion: {file_name}")
    except Exception as e:
        log(user_id, "notify_print_complete", f"Error notifying user about print completion: {e}")