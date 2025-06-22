from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards import main_menu_keyboard
from messages import MAIN_MENU_TEXT
from services.printer_status import get_printer_status

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    printer_msg = get_printer_status()
    await message.answer(MAIN_MENU_TEXT.format(printer_status=printer_msg), reply_markup=main_menu_keyboard)