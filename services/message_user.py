from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from decorators.admin_only import admin_only
from logger import log

router = Router()

class MessageUserState(StatesGroup):
    waiting_for_text = State()
    waiting_for_confirmation = State()

@router.message(Command("m"))
@admin_only
async def start_message_to_user(message: Message, state: FSMContext):
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("❌ Используй команду так: /m user_id")
        return

    user_id = int(parts[1])
    await state.set_state(MessageUserState.waiting_for_text)
    await state.update_data(target_user_id=user_id)
    await message.answer(f"✉️ Напиши сообщение, которое хочешь отправить пользователю <code>{user_id}</code>.")

@router.message(MessageUserState.waiting_for_text)
@admin_only
async def receive_message_text(message: Message, state: FSMContext):
    await state.update_data(message_text=message.text)
    await state.set_state(MessageUserState.waiting_for_confirmation)
    await message.answer(
        f"📨 Твоё сообщение:\n\n{message.text}\n\n✅ Подтвердить отправку? Напиши <b>да</b> или <b>нет</b>."
    )

@router.message(MessageUserState.waiting_for_confirmation, F.text.lower() == "да")
@admin_only
async def confirm_and_send(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data["target_user_id"]
    text = data["message_text"]

    try:
        await message.bot.send_message(chat_id=user_id, text=text)
        await message.answer("✅ Сообщение успешно отправлено.")
        log(message.from_user.id, "/m", f"Message sent to {user_id}: {text}")
    except Exception as e:
        await message.answer(f"❌ Не удалось отправить сообщение: {e}")
        log(message.from_user.id, "/m", f"Failed to send message to {user_id}: {e}")
    await state.clear()

@router.message(MessageUserState.waiting_for_confirmation, F.text.lower() == "нет")
@admin_only
async def cancel_send(message: Message, state: FSMContext):
    await message.answer("❌ Отправка отменена.")
    await state.clear()
