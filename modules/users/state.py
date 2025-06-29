from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.ui.main_menu import send_main_menu
from modules.analytics.logger import warning

class UserStates(StatesGroup):
    preview_before_payment = State()
    adjusting_print_settings = State()
    awaiting_page_range_input = State()  
    selecting_print_layout = State()
    waiting_for_method = State()
    waiting_for_cash_confirm = State()
    waiting_for_card_confirm = State()