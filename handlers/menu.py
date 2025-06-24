from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from messages import *
from keyboards import main_menu_keyboard
from callbacks import MAIN_MENU
from logger import log
from services.printer_status import get_printer_status

router = Router()

@router.callback_query(F.data ==MAIN_MENU)
async def handle_main_menu(callback: CallbackQuery):
    await callback.message.answer(
        text=MAIN_MENU_TEXT.format(printer_status=get_printer_status()),
        reply_markup=main_menu_keyboard
    )
    log(callback.from_user.id, MAIN_MENU, "Show main menu")

async def send_main_menu(bot: Bot, user_id: int, total_pages: int = 0):
    await bot.send_message(
        chat_id=user_id,
        text=MAIN_MENU_TEXT.format(printer_status=get_printer_status()),
        reply_markup=main_menu_keyboard
    )
