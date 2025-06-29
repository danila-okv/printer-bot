from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from .keyboard_tracker import send_managed_message
from .messages import *
from .callbacks import *
from modules.users.state import UserStates
from .keyboards import get_print_options_kb, return_kb, get_print_layouts_kb
from modules.analytics.logger import action, warning, error, info
from modules.decorators import check_paused
from modules.decorators import ensure_data    

router = Router()

# Handle Options
@router.callback_query(F.data == PRINT_OPTIONS)
@check_paused
@ensure_data
async def handle_print_options(callback: CallbackQuery, state: FSMContext, data: dict):    
    await state.set_state(UserStates.adjusting_print_settings)
    duplex = data.get("duplex", False)

    await callback.message.edit_text(
        text = get_print_options_text(data),
        reply_markup=get_print_options_kb(duplex)
    )
    action(
        user_id=callback.from_user.id,
        handler=PRINT_OPTIONS,
        msg="Started Option selection"
    )
    await callback.answer()

# Handle Pages option
@router.callback_query(F.data == OPTIONS_PAGES)
@check_paused
@ensure_data
async def handle_option_pages(callback: CallbackQuery, state: FSMContext, data: dict):
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
@check_paused
@ensure_data
async def handle_option_duplex(callback: CallbackQuery, state: FSMContext, data: dict):
    new = not data.get("duplex", False)
    await state.update_data(duplex=new)

    await callback.message.edit_reply_markup(reply_markup=get_print_options_kb(new))
    action(
        user_id=callback.from_user.id,
        handler=OPTIONS_DUPLEX,
        msg="Switched duplex option"
    )
    await callback.answer()

# Handle Layout option
@router.callback_query(F.data == OPTIONS_LAYOUT)
@check_paused
@ensure_data
async def handle_option_layout(callback: CallbackQuery, state: FSMContext, data: dict):
    layout = data.get("layout", "1")
    await callback.message.edit_text(
        text = get_print_layouts_text(data),
        reply_markup=get_print_layouts_kb(layout)
    )
    action(
        user_id=callback.from_user.id,
        handler=OPTIONS_LAYOUT,
        msg="Show layouts"
    )
    await callback.answer()
