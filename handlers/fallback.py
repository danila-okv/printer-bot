from aiogram import Router
from aiogram.types import Message
from messages import UNKNOWN_COMMAND_TEXT
from logger import log

router = Router()

@router.message()
async def unknown_message_handler(message: Message):
    log(message.from_user.id, "unknown_command", message.text)
    await message.answer(UNKNOWN_COMMAND_TEXT)