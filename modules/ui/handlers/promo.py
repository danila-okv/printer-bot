from aiogram import Router, F
from aiogram.types import Message
from modules.billing.services.promo import (
    promo_exists, promo_can_be_activated, has_activated_promo,
    get_promo_reward, record_promo_activation, add_user_bonus_pages
)
from modules.ui.keyboards.tracker import send_managed_message

router = Router()

@router.message(F.text.regexp(r"^[\w\dа-яА-ЯёЁ]{3,30}$"))
async def handle_promo_code_input(message: Message):
    code = message.text.strip()

    if not promo_exists(code):
        return  # Просто пропускаем — пусть другие обработчики ловят как обычный текст

    user_id = message.from_user.id

    if has_activated_promo(user_id, code):
        await message.answer("⚠️ Ты уже активировал этот промокод")
        return

    if not promo_can_be_activated(code):
        await message.answer("❌ Этот промокод больше не активен")
        return

    reward_type, reward_value = get_promo_reward(code)
    
    record_promo_activation(user_id, code)

    text = ""
    if reward_type == "pages":
        add_user_bonus_pages(user_id, int(reward_value))
        text = f"🎉 Промокод <b>{code}</b> активирован!\nТы получил <b>{int(reward_value)}</b> бесплатных страниц"
    elif reward_type == "discount":
        text = f"🎉 Промокод <b>{code}</b> активирован!\nТы получил скидку <b>{int(reward_value)}%</b>"

    await send_managed_message(
        bot=message.bot,
        user_id=user_id,
        text=text
    )