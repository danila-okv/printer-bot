from aiogram import Router

from .handlers import promo, cancel, confirm, fallback, file, main_menu, options, payment, back

router = Router()

for module in (promo, cancel, file, main_menu, payment, options, confirm, back, fallback):
    router.include_router(module.router)