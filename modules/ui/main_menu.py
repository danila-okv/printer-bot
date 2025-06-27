from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from ui.messages import *
from ui.keyboards import main_menu_kb
from ui.callbacks import MAIN_MENU
from analytics.logger import log
from printing.printer_status import get_printer_status
from ui.keyboard_tracker import send_managed_message
router = Router()

@router.callback_query(F.data ==MAIN_MENU)
async def handle_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text=MAIN_MENU_TEXT.format(printer_status=get_printer_status()),
        reply_markup=main_menu_kb
    )
    log(callback.from_user.id, MAIN_MENU, "Show main menu")

async def send_main_menu(bot: Bot, user_id: int, total_pages: int = 0):
    await send_managed_message(
        bot=bot,
        user_id=user_id,
        text=MAIN_MENU_TEXT.format(printer_status=get_printer_status()),
        reply_markup=main_menu_kb
    )
