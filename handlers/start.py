from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logger import log
from .main_menu import send_main_menu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    log(message.from_user.id, "start_command", "User started the bot")
    await state.clear()
    await send_main_menu(message.bot, message.from_user.id)