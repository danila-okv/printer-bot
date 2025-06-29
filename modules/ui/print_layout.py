from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from .messages import get_print_layouts_text
from .callbacks import LAYOUTS
from modules.users.state import UserStates
from .keyboards import get_print_layouts_kb
from modules.analytics.logger import action
from modules.decorators import ensure_data, check_paused
router = Router()

@router.callback_query(F.data.in_(LAYOUTS))
@check_paused
@ensure_data
async def handle_layout_selection(callback: CallbackQuery, state: FSMContext):
    await state.update_data(layout=callback.data)
    data = await state.get_data()
    await callback.message.edit_text(
        text=get_print_layouts_text(data),
        reply_markup=get_print_layouts_kb(callback.data)
    )

    action(
        callback.from_user.id,
        "print_layout",
        f"Select layout - {callback.data}"
    )
    callback.answer()
