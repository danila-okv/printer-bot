from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from .messages import *
from .keyboards import main_menu_kb
from .callbacks import MAIN_MENU
from modules.analytics.logger import log
from .keyboard_tracker import send_managed_message
router = Router()

@router.callback_query(F.data ==MAIN_MENU)
async def handle_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text=MAIN_MENU_TEXT,
        reply_markup=main_menu_kb
    )
    log(callback.from_user.id, MAIN_MENU, "Show main menu")

async def send_main_menu(bot: Bot, user_id: int, total_pages: int = 0):
    await send_managed_message(
        bot=bot,
        user_id=user_id,
        text=MAIN_MENU_TEXT,
        reply_markup=main_menu_kb
    )
