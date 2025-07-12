from aiogram import Router

from .handlers import cancel, confirm, fallback, file, main_menu, options, payment, back

router = Router()

for module in (cancel, file, main_menu, payment, options, confirm, back, fallback):
    router.include_router(module.router)