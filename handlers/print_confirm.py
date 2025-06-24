from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.print_service import add_job
from print_job import PrintJob
from handlers.menu import send_main_menu
from messages import *
from services.ledger import log_print_job
from callbacks import CONFIRM_PRINT
from logger import log

router = Router()

@router.callback_query(F.data == CONFIRM_PRINT)
async def handle_payment_confirmation(callback: CallbackQuery, state: FSMContext):
    
    """
    Обрабатывает нажатие кнопки «✅ Я оплатил»
    - достаёт данные из FSM
    - ставит в очередь печати
    - отправляет пользователю статус
    """
    log(callback.message.from_user.id, CONFIRM_PRINT)
    data = await state.get_data()
    await state.clear()

    file_path = data.get("file_path")
    page_count = data.get("page_count")
    file_name = data.get("file_name")

    payment_method = data.get("method", "card")  # card или "cash"
    log_print_job(
    user_id=callback.from_user.id,
    file_name=file_name,
    page_count=page_count,
    price=data.get("price", 0),
    method=payment_method
)

    if not all([file_path, page_count, file_name]):
        await callback.message.answer("❌ Ошибка: данные о файле утеряны. Начните заново.")
        await send_main_menu(callback.bot, callback.from_user.id)
        return

    # Создаём задание на печать
    job = PrintJob(
        user_id=callback.from_user.id,
        file_path=file_path,
        file_name=file_name,
        bot=callback.bot
    )

    add_job(job)
    await callback.message.edit_text("✅ Платёж подтверждён. Начинаю печать...")
