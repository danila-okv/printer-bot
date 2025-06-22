from aiogram.fsm.state import StatesGroup, State

class UserStates(StatesGroup):
    waiting_for_file = State()
    waiting_for_method = State()
    waiting_for_cash_confirm = State()
    waiting_for_card_confirm = State()
