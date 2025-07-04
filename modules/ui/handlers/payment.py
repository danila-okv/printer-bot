from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from modules.billing.ledger import log_print_job
from modules.printing.print_job import PrintJob
from modules.decorators import ensure_data
from modules.printing.print_service import add_job
from ..messages import *
from ..keyboards.payment import payment_methods_kb, payment_confirm_kb
from ..callbacks import *
from modules.users.state import UserStates
from modules.analytics.logger import action, warning, error, info
from modules.decorators import check_paused

router = Router()

# Cash payment handler
@router.callback_query(F.data == PAY_CASH)
@check_paused
@ensure_data
async def handle_cash_payment(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.update_data(method="cash")
    await state.set_state(UserStates.waiting_for_cash_confirm)

    await callback.message.edit_text(
        text=get_cash_payment_text(data),
        reply_markup=payment_confirm_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PAY_CASH,
        msg="Selected Cash payment method"
    )
    await callback.answer()


# Card payment handler
@router.callback_query(F.data == PAY_CARD)
@check_paused
@ensure_data
async def handle_card_payment(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.set_state(UserStates.waiting_for_cash_confirm)
    await state.update_data(method="card")

    await callback.message.edit_text(
        text=get_card_payment_text(data),
        reply_markup=payment_methods_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PAY_CARD,
        msg="Selected Card payment method"
    )
    await callback.answer()


# Pay with Alfa
@router.callback_query(F.data == PAY_ALFA)
@check_paused
@ensure_data
async def handle_alfa_payment(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.update_data(method="alfa")
    await state.set_state(UserStates.waiting_for_card_confirm)

    await callback.message.edit_text(
        text=get_alfa_payment_text(data),
        reply_markup=payment_confirm_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PAY_ALFA,
        msg="Selected Alfa payment method"
    )
    await callback.answer()
    


# Pay with Belarusbank
@router.callback_query(F.data == PAY_BELARUSBANK)
@check_paused
@ensure_data
async def handle_belarusbank_payment(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.update_data(method="belarusbank")
    await state.set_state(UserStates.waiting_for_card_confirm)

    await callback.message.edit_text(
        text=get_belarusbank_payment_text(data),
        reply_markup=payment_confirm_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PAY_BELARUSBANK,
        msg="Selected Belarusbank payment method"
    )
    await callback.answer()

# Pay with Other bank
@router.callback_query(F.data == PAY_OTHER)
@check_paused
@ensure_data
async def handle_other_payment(callback: CallbackQuery, state: FSMContext, data: dict):
    await state.update_data(method="other")
    await state.set_state(UserStates.waiting_for_card_confirm)

    await callback.message.edit_text(
        text=get_other_payment_text(data),
        reply_markup=payment_confirm_kb
    )
    action(
        user_id=callback.from_user.id,
        handler=PAY_OTHER,
        msg="Selected Other payment method"
    )
    await callback.answer()

# Pay confirm
@router.callback_query(F.data == PAY_CONFIRM)
@check_paused
@ensure_data
async def handle_pay_confirm(callback: CallbackQuery, state: FSMContext, data: dict):
    user_id = callback.from_user.id
    file_path = data.get("file_path")
    file_name = data.get("file_name")
    page_count = data.get("page_count")
    duplex = data.get("sides", False)
    layout = data.get("layout", "1")
    price = data.get("price")
    pages = data.get("pages")
    method = data.get("method", "cash")

    info(
        callback.from_user.id,
        PAY_CONFIRM,
        "Confirm payment"
    )

    log_print_job(
        user_id=user_id,
        file_name=file_name,
        page_count=page_count,
        price=price,
        method=method
    )

    job = PrintJob(
        user_id,
        file_path,
        file_name,
        callback.bot,
        page_count,
        duplex,
        layout,
        pages
    )
    
    add_job(job)
    info(
        user_id,
        PAY_CONFIRM,
        msg="Add Print Job"
    )

    await state.clear()
    await callback.answer(PAY_SUCCESS_TEXT)