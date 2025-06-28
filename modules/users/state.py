from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.ui.main_menu import send_main_menu

class UserStates(StatesGroup):
    preview_before_payment = State()
    adjusting_print_settings = State()
    awaiting_page_range_input = State()    
    waiting_for_method = State()
    waiting_for_cash_confirm = State()
    waiting_for_card_confirm = State()


REQUIRED_PRINT_FIELDS = ("file_name", "file_path", "page_count", "price")

async def ensure_print_data(state: FSMContext, callback: CallbackQuery) -> dict | None:
    data = await state.get_data()
    if not all(data.get(k) for k in REQUIRED_PRINT_FIELDS):
        await callback.message.answer("❌ Данные утеряны. Начни сначала.")
        await state.clear()
        await send_main_menu(callback.bot, callback.from_user.id)
        return None
    return data