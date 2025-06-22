import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.pdf_utils import get_page_count, is_supported_file, convert_docx_to_pdf
from services.price_calc import calculate_price
from keyboards import cancel_keyboard, payment_method_keyboard
from services.banlist import is_banned
from handlers.menu import send_main_menu
from states import UserStates
from callbacks import FILE_PRINT
from messages import *
from logger import log

router = Router()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.callback_query(F.data == FILE_PRINT)
async def handle_print_file(callback: Message, state: FSMContext):
    log(callback.from_user.id, FILE_PRINT, "User requested file print")
    await state.clear()
    await callback.message.edit_text(
        text=FILE_REQUEST_TEXT,
        reply_markup=cancel_keyboard
    )
    await state.set_state(UserStates.waiting_for_file)

@router.message(F.document)
async def handle_document(message: Message, state: FSMContext):
    log(message.from_user.id, f"handle_document", "User uploaded a document for printing, {doc.file_name}, {doc.file_size} bytes")
    doc = message.document
    original_file_name = doc.file_name

    user_id = message.from_user.id

    if is_banned(user_id):
        await message.answer("🚫 Вы были заблокированы. Обратитесь к администратору.")
        return

    if not is_supported_file(original_file_name):
        log(user_id, "handle_document", f"Unsupported file type: {original_file_name}")
        await message.answer(FILE_TYPE_ERROR_TEXT)
        return

    user_id = message.from_user.id
    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    uploaded_file_path = os.path.join(user_folder, original_file_name)

    processing_msg = await message.answer(FILE_PROCESSING_TEXT.format(file_name=original_file_name))

    try:
        tg_file = await message.bot.get_file(doc.file_id)
        log(user_id, "handle_document", f"Downloading file: {tg_file.file_path}")
        file_data = await message.bot.download_file(tg_file.file_path)
        with open(uploaded_file_path, "wb") as f:
            f.write(file_data.read())

        _, ext = os.path.splitext(original_file_name)
        ext = ext.lower()

        if ext == ".docx":
            # Конвертируем в data/tmp/converted.pdf для подсчёта страниц
            temp_pdf = await convert_docx_to_pdf(uploaded_file_path)

            # Формируем финальный путь с исходным именем, но расширением .pdf
            pdf_file_name = os.path.splitext(original_file_name)[0] + ".pdf"
            final_pdf_path = os.path.join(user_folder, pdf_file_name)
            os.replace(temp_pdf, final_pdf_path)
            processed_pdf_path = final_pdf_path
        else:
            processed_pdf_path = uploaded_file_path

        page_count, _ = await get_page_count(processed_pdf_path)
        price = calculate_price(page_count)

        await processing_msg.edit_text(
            FILE_PROCESSING_SUCCESS_TEXT.format(
                file_name=original_file_name,
                page_count=page_count,
                price=price,
            ),
            reply_markup=payment_method_keyboard
        )

        await state.set_state(UserStates.waiting_for_method)
        await state.update_data(
            price=price,
            file_path=processed_pdf_path,
            page_count=page_count,
            file_name=original_file_name,  # отображаемое имя
        )

    except Exception as err:
        await processing_msg.edit_text(FILE_PROCESSING_FAILURE_TEXT.format(file_name=original_file_name))
        await send_main_menu(message.bot, message.chat.id)
