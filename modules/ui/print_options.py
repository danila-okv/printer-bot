from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from modules.users.state import ensure_print_data
from .keyboard_tracker import send_managed_message
from .messages import *
from .callbacks import *
from modules.users.state import UserStates
from .keyboards import print_options_duplex_off_kb, print_options_duplex_on_kb, return_kb
from modules.analytics.logger import action, warning, error, info
router = Router()

# Handle Options
@router.callback_query(F.data == PRINT_OPTIONS)
async def handle_print_options(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return
    
    await state.set_state(UserStates.adjusting_print_settings)

    await callback.message.edit_text(
        text = get_print_options_text(data),
        reply_markup=print_options_duplex_on_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PRINT_OPTIONS,
        msg="Started Option selection"
    )
    await callback.answer()

# Handle Pages option
@router.callback_query(F.data == OPTIONS_PAGES)
async def handle_option_pages(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return

    await state.set_state(UserStates.awaiting_page_range_input)

    await send_managed_message(
        bot=callback.bot,
        user_id=callback.from_user.id,
        text="Range",
        reply_markup=return_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=OPTIONS_PAGES,
        msg="Selected Pages option"
    )
    await callback.answer()


# Handle Duplex option
@router.callback_query(F.data == OPTIONS_DUPLEX)
async def handle_option_duplex(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return
    
    new = not data.get("duplex", False)
    await state.update_data(duplex=new)

    kb = print_options_duplex_off_kb if new else print_options_duplex_on_kb
    await callback.message.edit_reply_markup(reply_markup=kb)
    action(
        user_id=callback.from_user.id,
        handler=OPTIONS_DUPLEX,
        msg="Switched duplex option"
    )
    await callback.answer()

# Handle Layout option
@router.callback_query(F.data == OPTIONS_LAYOUT)
async def handle_option_layout(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return
    
    await callback.message.edit_text(
        text = format_print_text(data) + "\n\nВыберите Layout:",
        reply_markup=print_options_duplex_on_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=OPTIONS_LAYOUT,
        msg="Selected Layout option"
    )
    await callback.answer()
