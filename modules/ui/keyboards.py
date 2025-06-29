
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from .messages import *
from .callbacks import *
from .buttons import *

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PROFILE, callback_data=PROFILE),
            InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv")
        ]
    ] 
)

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

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_ORDERDS, callback_data=ORDERS),
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN)
        ]
    ]
)

payment_confirm_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN),
            InlineKeyboardButton(text=BUTTON_CONFIRM, callback_data=PAY_CONFIRM)
        ]
    ]
)

payment_methods_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=BUTTON_PAY_ALFA, callback_data=PAY_ALFA),
            InlineKeyboardButton(text=BUTTON_PAY_BELARUSBANK, callback_data=PAY_BELARUSBANK)
        ],
        [   
            InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN),
            InlineKeyboardButton(text=BUTTON_PAY_OTHER, callback_data=PAY_OTHER)
        ]
    ]
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

# Print Options keyboards
def get_print_options_kb(duplex: bool) -> InlineKeyboardMarkup:
    duplex_text = BUTTON_OPTIONS_DUPLEX_DISABLED
    if duplex:
        duplex_text = BUTTON_OPTIONS_DUPLEX_ENABLED

    markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text=BUTTON_OPTIONS_LAYOUT, callback_data=OPTIONS_LAYOUT),
                InlineKeyboardButton(text=duplex_text, callback_data=OPTIONS_DUPLEX)
            ],
            [
                InlineKeyboardButton(text=BUTTON_RETURN, callback_data=RETURN),
                InlineKeyboardButton(text=BUTTON_OPTIONS_PAGES, callback_data=OPTIONS_PAGES)
            ]
        ]
    )
    return markup

def get_print_layouts_kb(selected_layout: str) -> InlineKeyboardMarkup:
    keyboard = []
    row = []

    for layout in LAYOUTS:
        # Добавляем галочку, если выбран
        layout_text = BUTTONS_LAYOUT.get(layout, "Unknown layout")
        text = f"✅ {layout_text}" if layout == selected_layout else f"📄 {layout_text}"

        button = InlineKeyboardButton(
            text=text,
            callback_data=layout
        )
        row.append(button)

        if len(row) == 2:
            keyboard.append(row)
            row = []

    # Добавляем последнюю неполную строку кнопок (если осталась одна)
    if row:
        keyboard.append(row)
        row = []

    # Добавляем кнопку "Назад"
    back_button = InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="go_back"
    )

    # Если последняя строка пустая — создаём новую строку, иначе — добавляем в текущую
    if not keyboard or len(keyboard[-1]) == 2:
        keyboard.append([back_button])
    else:
        keyboard[-1].append(back_button)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)