from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from messages import *

router = Router()

# ─────────────────────────────────────────────────────────────
# Главное меню — клавиатура
# ─────────────────────────────────────────────────────────────
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTON_SETTINGS, callback_data="settings"), InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv")],
        [InlineKeyboardButton(text=BUTTON_PRINT_FILE, callback_data="start_print")]
    ])

# ─────────────────────────────────────────────────────────────
# Отправка главного меню (используется другими модулями)
# ─────────────────────────────────────────────────────────────
async def send_main_menu(bot: Bot, user_id: int, total_pages: int = 0):
    await bot.send_message(
        chat_id=user_id,
        text=MAIN_MENU_TEXT.format(total_pages=total_pages),
        reply_markup=get_main_menu_keyboard()
    )

# ─────────────────────────────────────────────────────────────
# Обработка кнопки «Напечатать файл» → сбрасывает FSM
# ─────────────────────────────────────────────────────────────
@router.callback_query(F.data == "start_print")
async def handle_start_print(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text=FILE_REQUEST_TEXT,
        reply_markup=None
    )
