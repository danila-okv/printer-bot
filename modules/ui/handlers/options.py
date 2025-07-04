from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from modules.decorators import ensure_data
from modules.users.state import UserStates
from ..keyboards.common import return_kb
from ..keyboards.options import get_print_options_kb, get_print_layouts_kb, confim_page_ranges_kb
from ..keyboards.tracker import send_managed_message
from modules.analytics.logger import action, warning, error, info
from modules.decorators import check_paused
from utils.parsers import validate_page_range_str


from ..messages import (
    get_print_options_text, get_layout_selection_text, get_pages_input_text,

)
from ..callbacks import (
    PRINT_OPTIONS, OPTION_DUPLEX, OPTION_LAYOUT, OPTION_PAGES,
    LAYOUTS
)

router = Router()

# Handle Options
@router.callback_query(F.data == PRINT_OPTIONS)
@check_paused
@ensure_data
async def handle_print_options(callback: CallbackQuery, state: FSMContext, data: dict):    
    await state.set_state(UserStates.adjusting_print_options)
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

# Handle Duplex option
@router.callback_query(F.data == OPTION_DUPLEX)
@check_paused
@ensure_data
async def handle_option_duplex(callback: CallbackQuery, state: FSMContext, data: dict):
    new = not data.get("duplex", False)
    await state.update_data(duplex=new)
    data["duplex"] = new


    await callback.message.edit_text(
        text=get_print_options_text(data),
        reply_markup=get_print_options_kb(new)
        )
    action(
        user_id=callback.from_user.id,
        handler=OPTION_DUPLEX,
        msg="Switched duplex option"
    )
    await callback.answer()

# Handle Layout option
@router.callback_query(F.data == OPTION_LAYOUT)
@check_paused
@ensure_data
async def handle_option_layout(callback: CallbackQuery, state: FSMContext, data: dict):
    layout = data.get("layout", "1")
    await callback.message.edit_text(
        text = get_layout_selection_text(data),
        reply_markup=get_print_layouts_kb(layout)
    )
    action(
        user_id=callback.from_user.id,
        handler=OPTION_LAYOUT,
        msg="Show layouts"
    )
    await callback.answer()

# Handle Layouts selection
@router.callback_query(F.data.in_(LAYOUTS))
@check_paused
@ensure_data
async def handle_layout_selection(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.update_data(layout=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(
        text=get_layout_selection_text(data),
        reply_markup=get_print_layouts_kb(callback.data)
    )
    await callback.answer()

    action(
        callback.from_user.id,
        "print_layout",
        f"Select layout - {callback.data}"
    )

# Handle Pages option
@router.callback_query(F.data == OPTION_PAGES)
@check_paused
@ensure_data
async def handle_pages_selection(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.set_state(UserStates.awaiting_page_range_input)

    await callback.message.edit_text(
        text=get_pages_input_text(data),
        reply_markup=return_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=OPTION_PAGES,
        msg="Select Pages option"
    )
    callback.answer()

# Handle Page ranges input
@router.message(UserStates.awaiting_page_range_input)
@check_paused
@ensure_data
async def handle_page_ranges_input(message: Message, state: FSMContext, data: dict):
    text = message.text.strip()

    page_count = data.get("page_count", 0)

    try:
        pages = validate_page_range_str(text, page_count)
        await state.update_data(selected_pages=pages)
        
        await send_managed_message(
            bot=message.bot,
            user_id=message.from_user.id,
            text=f"Приняты страницы: {pages}",
            reply_markup=confim_page_ranges_kb
        )
    except ValueError as e:
        await message.answer(f"Ошибка: {e}")