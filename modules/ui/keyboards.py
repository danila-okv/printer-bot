
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from ui.messages import *
from ui.callbacks import *
from ui.buttons import *

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PROFILE, callback_data=PROFILE),
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv")
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

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_ORDERDS, callback_data=ORDERS),
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN)
        ]
    ]
)

pay_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL),
            InlineKeyboardButton(text=BUTTON_CONFIRM, callback_data=PAY_CONFIRM)
        ]
    ]
)

pay_methods_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PAY_ALFA, callback_data=PAY_ALFA),
            InlineKeyboardButton(text=BUTTON_PAY_BELARUSBANK, callback_data=PAY_BELARUSBANK)
        ],
        [   
            InlineKeyboardButton(text=BUTTON_PAY_OTHER, callback_data=PAY_OTHER),
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=RETURN)
        ]
    ]
)

# TODO: Remove when payment_method_kb will confirm printing
print_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_CONFIRM, callback_data=CONFIRM),
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)

print_preview_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTON_PRINT_OPTIONS, callback_data=PRINT_OPTIONS)],
        [InlineKeyboardButton(text=BUTTON_PAY_CASH, callback_data=PAY_CASH),
         InlineKeyboardButton(text=BUTTON_PAY_CARD, callback_data=PAY_CARD)
         ],
        [InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)]
    ]
)

print_options_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=BUTTON_OPTIONS_PAGES, callback_data=OPTIONS_PAGES)],
        [InlineKeyboardButton(text=BUTTON_OPTIONS_DUPLEX, callback_data=OPTIONS_DUPLEX)],
        [InlineKeyboardButton(text=BUTTON_OPTIONS_LAYOUT, callback_data=OPTIONS_LAYOUT)],
        [
            InlineKeyboardButton(text=BUTTON_DONE, callback_data=DONE),
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN)
        ]
    ]
)

print_done_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv"),
            InlineKeyboardButton(text=BUTTON_DONE, callback_data=DONE)
        ]
    ]
)

print_error_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv"),
            InlineKeyboardButton(text=BUTTON_CANCEL, callback_data=CANCEL)
        ]
    ]
)
