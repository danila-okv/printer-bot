from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.ui.handlers.main_menu import send_main_menu
from modules.analytics.logger import warning

class UserStates(StatesGroup):
    reviewing_print_details = State()
    setting_print_options = State()
    inputting_pages = State()
    inputting_copies_count = State()
    confirming_pages = State()
    selecting_print_layout = State()
    selecting_payment_option = State()
    confirming_cash_payment = State()
    confirming_card_payment = State()

class PromoStates(StatesGroup):
    choosing_type = State()
    entering_activations = State()
    entering_expires_at = State()
    entering_duration = State()
    entering_reward_value = State()
    confirming = State()