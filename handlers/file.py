import os
import logging

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.pdf_utils import get_page_count, is_supported_file
from services.price_calc import calculate_price
from handlers.payment import PaymentMethod, get_payment_method_keyboard
from keyboards import cancel_keyboard
from handlers.menu import send_main_menu
from callbacks import FILE_PRINT
from messages import *

router = Router()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.callback_query(F.data == FILE_PRINT)
async def handle_print_file(callback: Message, state: FSMContext):
    """
    Обрабатывает нажатие кнопки «Напечатать файл»:
    - очищает FSM
    - отправляет сообщение с просьбой загрузить файл
    """
    await state.clear()
    await callback.message.edit_text(
        text=FILE_REQUEST_TEXT,
        reply_markup=cancel_keyboard
    )
    await state.set_state(PaymentMethod.waiting_for_file)
    logging.info("FSM cleared and waiting for file upload.") 

@router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    """
    Принимает .pdf или .docx, сохраняет, считает страницы, показывает стоимость,
    предлагает выбрать метод оплаты прямо в том же сообщении.
    """
    doc = message.document
    file_name = doc.file_name

    # ── Проверка поддерживаемого формата
    if not is_supported_file(file_name):
        await message.answer(FILE_TYPE_ERROR_TEXT)
        return

    # ── Подготовка пути
    user_id = message.from_user.id
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file_name)

    # ── Отправляем сообщение "Обрабатываю..."
    processing_msg = await message.answer(FILE_PROCESSING_TEXT.format(file_name=file_name))

    try:
        # ── Скачиваем файл
        tg_file = await message.bot.get_file(doc.file_id)
        file_data = await message.bot.download_file(tg_file.file_path)
        with open(file_path, "wb") as f:
            f.write(file_data.read())

        # ── Подсчёт страниц и стоимости
        page_count, processed_pdf = await get_page_count(file_path)
        price = calculate_price(page_count)

        # ── Обновляем сообщение: успех + кнопки
        await processing_msg.edit_text(
            FILE_PROCESSING_SUCCESS_TEXT.format(
                file_name=file_name,
                page_count=page_count,
                price=price,
            ),
            reply_markup=get_payment_method_keyboard()
        )

        # ── Сохраняем в FSM данные на этапе выбора метода оплаты
        await state.set_state(PaymentMethod.waiting_for_method)
        await state.update_data(
            price=price,
            file_path=processed_pdf,
            page_count=page_count,
            file_name=file_name,
        )

    except Exception as err:
        logging.exception("Ошибка при обработке файла: %s", err)
        await processing_msg.edit_text(FILE_PROCESSING_FAILURE_TEXT.format(file_name=file_name))
        await send_main_menu(message.bot, message.chat.id)
