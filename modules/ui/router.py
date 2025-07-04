from aiogram import Router

from .handlers import cancel, fallback, file, main_menu, options, payment

from .handlers import return_handler

router = Router()

for module in (cancel, file, main_menu, payment, options, return_handler, fallback):
    router.include_router(module.router)