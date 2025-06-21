from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import main_menu_keyboard
from messages import MAIN_MENU_TEXT

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(MAIN_MENU_TEXT, reply_markup=main_menu_keyboard)