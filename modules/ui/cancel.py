from aiogram import Router
from aiogram.types import Message
from aiogram import Router, F
from aiogram.types import CallbackQuery
from ui.main_menu import send_main_menu
from ui.callbacks import CANCEL
from ui.messages import PRINT_CANCELLED_TEXT
from analytics.logger import log

router = Router()

@router.callback_query(F.data == CANCEL)
async def start_command(callback: CallbackQuery):
    log(callback.from_user.id, CANCEL, "User cancelled the print")
    await callback.message.edit_text(text=PRINT_CANCELLED_TEXT)
    await send_main_menu(callback.bot, callback.from_user.id)