from aiogram import Router

from .handlers import (
    ban, control, promo, shell,message_user

)

router = Router()

for module in (ban, control, promo, shell, message_user):
    router.include_router(module.router)