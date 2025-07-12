from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from modules.ui.keyboards.admin import promo_type_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from modules.ui.keyboards.tracker import send_managed_message
from modules.admin.services.promo import create_promo, promo_exists
from modules.decorators import admin_only
from states import PromoStates
from datetime import datetime

router = Router()


@router.message(Command("promo"))
@admin_only
async def cmd_promo(message: Message, state: FSMContext):
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("⚠️ Использование: /promo [код]")

    code = parts[1].strip()

    if promo_exists(code):
        return await message.reply(f"❌ Промокод <b>{code}</b> уже существует")
    
    await state.update_data(code=code)
    await state.set_state(PromoStates.choosing_type)

    await send_managed_message(
        message.bot,
        message.from_user.id,
        f"Вы создали новый промокод: <b>{code}</b>\n"
             "Теперь выбери тип награды для этого промокода.",
        promo_type_kb
    )

@router.callback_query(PromoStates.choosing_type)
async def promo_choose_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(reward_type=callback.data)
    await state.set_state(PromoStates.entering_activations)
    await callback.message.edit_text("Введи общее количество активаций промокода:")

@router.message(PromoStates.entering_activations)
async def promo_enter_activations(message: Message, state: FSMContext):
    try:
        count = int(message.text.strip())
        if count < 1:
            raise ValueError()
    except:
        return await message.reply("❌ Введи положительное число активаций")
    await state.update_data(activations_total=count)
    data = await state.get_data()
    if data['reward_type'] == 'bonus_pages':
        await message.answer("Введи количество страниц в качестве награды:")
    else:
        await message.answer("Введи процент скидки в качестве награды (от 1% до 100%):")
    await state.set_state(PromoStates.entering_reward_value)

@router.message(PromoStates.entering_reward_value)
async def promo_enter_reward_value(message: Message, state: FSMContext):
    text = message.text.strip().replace(",", ".").replace(" ", "")
    if text.endswith("%"):
        text = text[:-1]

    try:
        value = float(text)
        if value <= 0 or value > 100:
            raise ValueError()
    except ValueError:
        return await message.reply("❌ Введи корректное значение скидки от 1 до 100% (например, 30%)")

    await state.update_data(reward_value=value)
    await state.set_state(PromoStates.entering_expires_at)
    await message.answer("Введи дату окончания действия промокода (ГГГГ-ММ-ДД) или напиши «нет», чтобы не ограничивать:")

@router.message(PromoStates.entering_expires_at)
async def promo_enter_expires_at(message: Message, state: FSMContext):
    text = message.text.strip().lower()
    if text in ("нет", "none", "-"):
        await state.update_data(expires_at=None)
    else:
        try:
            dt = datetime.strptime(text, "%Y-%m-%d")
            await state.update_data(expires_at=dt.strftime("%Y-%m-%d"))
        except:
            return await message.reply("❌ Неверный формат даты. Используй ГГГГ-ММ-ДД или напиши «нет»")
    
    data = await state.get_data()
    txt = f"""Подтверди создание промокода:

🔑 <b>{data['code']}</b>
🎁 Тип: {'Страницы' if data['reward_type']=='bonus_pages' else 'Скидка'}
📊 Значение: {data['reward_value']}
🔁 Активаций: {data['activations_total']}
⏳ Действует до: {data['expires_at'] or 'Без ограничений'}

Подтвердить?"""

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_promo")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_promo")]
    ])
    await state.set_state(PromoStates.confirming)
    await message.answer(txt, reply_markup=kb)



@router.callback_query(PromoStates.confirming)
async def promo_final_confirm(callback: CallbackQuery, state: FSMContext):
    if callback.data == "cancel_promo":
        await state.clear()
        return await callback.message.edit_text("🚫 Отменено.")

    data = await state.get_data()
    create_promo(
        code=data['code'],
        activations_total=data['activations_total'],
        reward_type=data['reward_type'],
        reward_value=data['reward_value'],
        expires_at=data['expires_at']
    )
    await state.clear()
    await callback.message.edit_text("🎉 Промокод успешно создан!")
