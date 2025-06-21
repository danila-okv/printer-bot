from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from messages import *
from keyboards import main_menu_keyboard
from callbacks import MAIN_MENU

router = Router()

@router.callback_query(F.data ==MAIN_MENU)
def handle_main_menu(callback: CallbackQuery):
    """
    Обрабатывает нажатие кнопки «Главное меню»
    - отправляет главное меню
    """
    callback.message.answer(
        text=MAIN_MENU_TEXT,
        reply_markup=main_menu_keyboard
    )

async def send_main_menu(bot: Bot, user_id: int, total_pages: int = 0):
    await bot.send_message(
        chat_id=user_id,
        text=MAIN_MENU_TEXT,
        reply_markup=main_menu_keyboard
    )
