from aiogram import Bot
from keyboards import print_done_keyboard
from messages import PRINT_DONE_TEXT
import logging

async def notify_print_complete(user_id: int, bot: Bot, file_name: str):
    try:
        await bot.send_message(
            chat_id=user_id,
            text=PRINT_DONE_TEXT.format(file_name=file_name),
            reply_markup=print_done_keyboard
        )
        logging.info(f"Пользователь {user_id} уведомлён о завершении печати файла: {file_name}")
    except Exception as e:
        logging.exception(f"Ошибка при уведомлении пользователя {user_id}: {e}")