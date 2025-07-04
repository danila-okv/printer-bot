
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ..callbacks import (
    PRINT_OPTIONS, PAY_CASH, PAY_CARD, CANCEL
)
from .buttons import (
    BUTTON_PRINT_OPTIONS, BUTTON_PAY_CASH, BUTTON_PAY_CARD, BUTTON_CANCEL
)

print_preview_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTON_PRINT_OPTIONS, callback_data=PRINT_OPTIONS)],
        [
            InlineKeyboardButton(text=BUTTON_PAY_CASH, callback_data=PAY_CASH),
            InlineKeyboardButton(text=BUTTON_PAY_CARD, callback_data=PAY_CARD)
        ],
        [InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)]
    ]
)