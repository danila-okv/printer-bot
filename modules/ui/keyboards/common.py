
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from ..callbacks import RETURN, CANCEL
from .buttons import BUTTON_RETURN, BUTTON_CANCEL

return_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN)
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