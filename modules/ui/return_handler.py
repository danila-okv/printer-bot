from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.users.state import UserStates, ensure_print_data
from .keyboards import print_options_duplex_off_kb, print_preview_kb, pay_methods_kb
from .messages import *
from .callbacks import RETURN
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.callback_query(F.data == RETURN)
async def handle_return(callback: CallbackQuery, state: FSMContext):

    current = await state.get_state()
    data = await state.get_data()

    if current == UserStates.adjusting_print_settings:
        await state.set_state(UserStates.preview_before_payment)

        await callback.message.edit_text(
            text=format_print_text(data),
            reply_markup=print_preview_kb
        )
        return await callback.answer()
    
    # Handle return from Page range or Layout options
    if current == UserStates.awaiting_page_range_input or current == UserStates.selecting_print_layout:
        await state.set_state(UserStates.adjusting_print_settings)

        await callback.message.edit_text(
            text=get_print_options_text(data),
            reply_markup=print_options_duplex_off_kb
        )
        return await callback.answer()
    
    # Handle return from Cash confirmation
    if current == UserStates.waiting_for_cash_confirm:
        await state.set_state(UserStates.preview_before_payment)

        await callback.message.edit_text(
            text=get_print_preview_text(data),
            reply_markup=print_preview_kb
        )
        return await callback.answer()
    
    if current == UserStates.waiting_for_card_confirm and data["method"] == "card":
        await state.set_state(UserStates.preview_before_payment)

        await callback.message.edit_text(
            text=get_print_preview_text(data),
            reply_markup=print_preview_kb
        )
        return await callback.answer()
    
    if current == UserStates.waiting_for_card_confirm and data["method"] != "card":
        await state.update_data(method="card")

        await callback.message.edit_text(
            text=get_print_preview_text(data),
            reply_markup=pay_methods_kb
        )
        return await callback.answer()

