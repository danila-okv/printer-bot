from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from modules.billing.ledger import log_print_job
from modules.printing.print_job import PrintJob
from modules.users.state import ensure_print_data
from modules.printing.print_service import add_job
from .messages import *
from .keyboards import pay_methods_kb, pay_confirm_kb
from .callbacks import *
from modules.users.state import UserStates
from modules.analytics.logger import log

router = Router()

# Cash payment handler
@router.callback_query(F.data == PAY_CASH)
async def handle_cash_payment(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return
    
    callback.message.edit_text()
    await callback.message.edit_text(
        text=PAY_CASH_TEXT.format(file_name=data["file_name"], page_count=data["page_count"], price=data["price"]),
        reply_markup=pay_confirm_kb
    )
    log(callback.message.from_user.id, PAY_CASH, "User select Cash payment")
    await state.update_data(method="cash")
    await state.set_state(UserStates.waiting_for_cash_confirm)

# Card payment handler
@router.callback_query(F.data == PAY_CARD)
async def handle_card_payment(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return 
    await callback.message.edit_text(
        text=PAY_CARD_TEXT.format(file_name=data["file_name"], page_count=data["page_count"], price=data["price"]),
        reply_markup=pay_methods_kb
    )
    log(callback.message.from_user.id, PAY_CARD, "User select Card payment")
    await state.update_data(method="card")

# Pay with Alfa
@router.callback_query(F.data == PAY_ALFA)
async def handle_alfa_payment(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return 
    await callback.message.edit_text(
        text=PAY_ALFA_TEXT.format(file_name=data["file_name"], page_count=data["page_count"], price=data["price"]),
        reply_markup=pay_confirm_kb
    )
    log(callback.message.from_user.id, PAY_CASH, "User select Cash payment")
    await state.update_data(method="alfa")
    await state.set_state(UserStates.waiting_for_card_confirm)

# Pay with Belarusbank
@router.callback_query(F.data == PAY_BELARUSBANK)
async def handle_belarusbank_payment(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return 
    await callback.message.edit_text(
        text=PAY_BELARUSBANK_TEXT.format(file_name=data["file_name"], page_count=data["page_count"], price=data["price"]),
        reply_markup=pay_confirm_kb
    )
    log(callback.message.from_user.id, PAY_CASH, "User select Cash payment")
    await state.update_data(method="belarusbank")
    await state.set_state(UserStates.waiting_for_card_confirm)

# Pay with Other bank
@router.callback_query(F.data == PAY_OTHER)
async def handle_other_payment(callback: CallbackQuery, state: FSMContext):
    data = await ensure_print_data(state, callback)
    if data is None:
        return 
    await callback.message.edit_text(
        text=PAY_OTHER_TEXT.format(file_name=data["file_name"], page_count=data["page_count"], price=data["price"]),
        reply_markup=pay_confirm_kb
    )
    log(callback.message.from_user.id, PAY_OTHER, "User select Other bank to pay")
    await state.update_data(method="other")
    await state.set_state(UserStates.waiting_for_card_confirm)

# Pay confirm
@router.callback_query(F.data == PAY_CONFIRM)
async def handle_pay_confirm(callback: CallbackQuery, state: FSMContext):
    log(callback.from_user.id, PAY_CONFIRM)
    data = await ensure_print_data(state, callback)
    if data is None:
        return 
    
    user_id = callback.from_user.id
    file_path = data.get("file_path")
    file_name = data.get("file_name")
    page_count = data.get("page_count")
    price = data.get("price")
    method = data.get("method", "unknown")

    log_print_job(
        user_id=user_id,
        file_name=file_name,
        page_count=page_count,
        price=price,
        method=method
    )

    job = PrintJob(
        user_id=user_id,
        file_path=file_path,
        file_name=file_name,
        bot=callback.bot
    )
    add_job(job)

    await state.clear()
    await callback.message.edit_text(PAY_SUCCESS_TEXT)