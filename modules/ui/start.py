from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from modules.analytics.logger import action
from .main_menu import send_main_menu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    
    await state.clear()
    await send_main_menu(message.bot, message.from_user.id)
    action(
        user_id=message.from_user.id,
        handler="Command /start",
        msg="User started bot"
    )