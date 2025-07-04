
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from ..callbacks import BACK, CANCEL
from .buttons import BUTTON_RETURN, BUTTON_CANCEL

return_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=BACK)
        ]
    ] 
)

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)