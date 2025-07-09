from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..callbacks import ORDERS, BACK
from .buttons import BUTTON_ORDERDS, BUTTON_BACK


profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_ORDERDS, callback_data=ORDERS),
            InlineKeyboardButton(text=BUTTON_BACK, callback_data=BACK)
        ]
    ]
)
