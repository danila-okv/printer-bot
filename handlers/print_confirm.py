# handlers/print_confirm.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from services.print_service import PrintJob, print_manager
from handlers.payment import send_main_menu
from handlers.payment import PaymentMethod
from messages import *

router = Router()


@router.callback_query(F.data == "confirm_payment")
async def handle_payment_confirmation(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки «✅ Я оплатил»
    - достаёт данные из FSM
    - ставит в очередь печати
    - отправляет пользователю статус
    """
    print("[DEBUG] handle_payment_confirmation called")
    data = await state.get_data()
    await state.clear()

    file_path = data.get("file_path")
    page_count = data.get("page_count")
    file_name = data.get("file_name")

    if not all([file_path, page_count, file_name]):
        await callback.message.answer("❌ Ошибка: данные о файле утеряны. Начните заново.")
        await send_main_menu(callback.bot, callback.from_user.id)
        return

    # Создаём задание на печать
    job = PrintJob(
        user_id=callback.from_user.id,
        file_path=file_path,
        file_name=file_name,
        page_count=page_count,
        bot=callback.bot
    )

    position = await print_manager.add_job(job)

    if position == 1:
        await callback.message.edit_text("✅ Платёж подтверждён. Начинаю печать...")
    else:
        await callback.message.edit_text(
            f"✅ Платёж подтверждён.\n📑 Файл поставлен в очередь (позиция {position})."
        )
