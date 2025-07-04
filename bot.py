import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Роутеры
from modules.notifications import message_user
from modules.analytics import analytics
from modules.admin import panel, shell, printer
from modules.ui.router import router as ui_router

from db import init_db

if __name__ == "__main__":
    init_db()

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Главная асинхронная функция
async def main():
    logging.basicConfig(level=logging.INFO)

    # Создаём бота и диспетчер
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем обработчики
    
    dp.include_router(panel.router)
    dp.include_router(analytics.router)
    dp.include_router(message_user.router)
    dp.include_router(shell.router)
    dp.include_router(printer.router)
    dp.include_router(ui_router)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
