from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from messages import *
from handlers.payment import send_main_menu

router = Router()

@router.message(F.text == "/start")
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    await send_main_menu(
        bot=message.bot,
        user_id=message.from_user.id,
        total_pages=0  # можно потом подставить реальную статистику
    )