
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from messages import *
from callbacks import *

main_menu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [ 
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv"),
            InlineKeyboardButton(text=BUTTON_PRINT_FILE, callback_data=FILE_PRINT)
        ]
    ] 
)

cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)

payment_method_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_METHOD_CASH, callback_data=PAY_CASH),
            InlineKeyboardButton(text=BUTTON_METHOD_CARD, callback_data=PAY_CARD)
        ],
        [
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)

print_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PRINT_CONFIRM, callback_data=CONFIRM_PRINT),
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)

print_done_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_MENU, callback_data=MAIN_MENU),
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv")
        ]
    ]
)

print_error_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv"),
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)
