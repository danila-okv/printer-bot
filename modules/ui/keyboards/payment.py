from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..callbacks import (PAY_ALFA, PAY_BELARUSBANK, PAY_OTHER, PAY_CONFIRM, BACK)
from .buttons import (BUTTON_PAY_ALFA, BUTTON_PAY_BELARUSBANK, BUTTON_PAY_OTHER, BUTTON_CONFIRM, BUTTON_RETURN)

payment_methods_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PAY_ALFA, callback_data=PAY_ALFA),
            InlineKeyboardButton(text=BUTTON_PAY_BELARUSBANK, callback_data=PAY_BELARUSBANK)
        ],
        [   
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=BACK),
            InlineKeyboardButton(text=BUTTON_PAY_OTHER, callback_data=PAY_OTHER)
        ]
    ]
)

payment_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=BACK),
            InlineKeyboardButton(text=BUTTON_CONFIRM, callback_data=PAY_CONFIRM)
        ]
    ]
)