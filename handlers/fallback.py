from aiogram import Router
from aiogram.types import Message
from messages import UNKNOWN_COMMAND_TEXT

router = Router()

@router.message()
async def unknown_message_handler(message: Message):
    await message.answer(UNKNOWN_COMMAND_TEXT)