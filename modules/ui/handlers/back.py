from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.users.state import UserStates
from modules.decorators import ensure_data
from modules.decorators import check_paused
from ..keyboards.preview import print_preview_kb
from ..keyboards.payment import payment_methods_kb
from ..keyboards.options import get_print_options_kb
from ..messages import *
from ..callbacks import BACK
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.callback_query(F.data == BACK)
@check_paused
@ensure_data
async def handle_return(callback: CallbackQuery, state: FSMContext, data: dict):
    current = await state.get_state()

    if current == UserStates.adjusting_print_options:
        await state.set_state(UserStates.preview_before_payment)

        await callback.message.edit_text(
            text=format_print_text(data),
            reply_markup=print_preview_kb
        )
        return await callback.answer()
    
    # Handle return from Page range or Layout options
    if current == UserStates.awaiting_page_range_input or current == UserStates.selecting_print_layout:
        await state.set_state(UserStates.adjusting_print_options)
        duplex = data.get("duplex", False)

        await callback.message.edit_text(
            text=get_print_options_text(data),
            reply_markup=get_print_options_kb(duplex)
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
            text=get_card_payment_text(data),
            reply_markup=payment_methods_kb
        )
        return await callback.answer()
