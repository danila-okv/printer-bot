from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from modules.users.state import UserStates
from modules.decorators import ensure_data
from modules.decorators import check_paused
from modules.analytics.logger import action, warning, error
from ..keyboards.review import details_review_kb
from ..keyboards.payment import payment_methods_kb
from ..keyboards.options import get_print_options_kb
from ..messages import (
    get_print_options_text
)
from ..callbacks import CONFIRM
from utils.parsers import validate_page_range_str
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.callback_query(F.data == CONFIRM)
@check_paused
@ensure_data
async def handle_confirm(callback: CallbackQuery, state: FSMContext, data: dict):
    current = await state.get_state()
    print(f"Current state: {current}")
    if current == UserStates.inputting_copies_count:
        copies = data.get("copies", 1)
        if not isinstance(copies, int) or copies <= 0:
            await callback.answer("Количество копий должно быть положительным числом.")
            warning(
                callback.from_user.id,
                handler=CONFIRM,
                msg=f"Invalid copies count: {copies}"
            )
            return

        await state.update_data(copies=copies)

        try:
            await callback.message.edit_text(
                text=get_print_options_text(data),
                reply_markup=details_review_kb
            )
        except TelegramBadRequest as e:
            await callback.message.answer(f"Ошибка при обновлении текста: {e}")
            error(
                callback.from_user.id,
                CONFIRM,
                f"Error updating text: {e}"
            )
            return

        await state.set_state(UserStates.setting_print_options)
        action(
            callback.from_user.id,
            CONFIRM,
            f"Copies count confirmed: {copies}"
        )
        return await callback.answer()
    
    if current == UserStates.inputting_pages:
        pages = data.get("pages", "")
        if not validate_page_range_str(pages):
            await callback.message.answer("Некорректный диапазон страниц.")
            warning(
                callback.from_user.id,
                handler=CONFIRM,
                msg=f"Invalid page range: {pages}"
            )
            return

        await state.update_data(pages=pages)

        try:
            await callback.message.edit_text(
                text=get_print_options_text(data),
                reply_markup=details_review_kb
            )
        except TelegramBadRequest as e:
            await callback.message.answer(f"Ошибка при обновлении текста: {e}")
            error(
                callback.from_user.id,
                handler=CONFIRM,
                msg=f"Error updating text: {e}"
            )
            return

        await state.set_state(UserStates.setting_print_options)
        action(
            callback.from_user.id,
            CONFIRM,
            f"Pages confirmed: {pages}"
        )
        return await callback.answer()