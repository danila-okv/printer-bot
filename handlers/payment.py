# handlers/payment.py

from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from messages import *
from keyboards import main_menu_keyboard, print_confirm_keyboard
from callbacks import *

router = Router()

# Card payment handler
@router.callback_query(F.data == PAY_CARD)
async def handle_card_payment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=PAYMENT_CARD_TEXT,
        reply_markup=print_confirm_keyboard
    )
    await state.update_data(method="card")


# Cash payment handler
@router.callback_query(F.data == PAY_CASH)
async def handle_cash_payment(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text=PAYMENT_CASH_TEXT,
        reply_markup=print_confirm_keyboard
    )
    await state.update_data(method="cash")