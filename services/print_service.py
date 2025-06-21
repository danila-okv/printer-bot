# services/print_service.py

import asyncio
from collections import deque
from dataclasses import dataclass
from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
)
import subprocess
from messages import *

@dataclass
class PrintJob:
    user_id: int
    file_path: str
    file_name: str
    page_count: int
    bot: any  # aiogram.Bot

class PrintManager:
    def __init__(self, print_speed_sec_per_page=5):
        self.queue = deque()
        self.is_printing = False
        self.print_speed = print_speed_sec_per_page  # в секундах

    async def add_job(self, job: PrintJob) -> int:
        """
        Добавляет задание в очередь.
        Если очередь пуста — запускает печать.
        Возвращает позицию в очереди (1 = печатаем сразу).
        """
        self.queue.append(job)
        position = len(self.queue)

        if not self.is_printing:
            asyncio.create_task(self._start_printing())

        return position

    async def _start_printing(self):
        self.is_printing = True

        while self.queue:
            job = self.queue.popleft()

            try:
                est_time = job.page_count * self.print_speed
                await job.bot.send_message(
                    chat_id=job.user_id,
                    text=f"🖨️ Печатаю <b>{job.file_name}</b>\n⏳ Примерное время: <b>{est_time} сек.</b>"
                )

                await self._print_file(job.file_path)

                await job.bot.send_message(
                    chat_id=job.user_id,
                    text=PRINT_DONE_TEXT
                )
            except Exception as e:
                await job.bot.send_message(
                    chat_id=job.user_id,
                    text=f"❌ Ошибка при печати: {e}",
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text=BUTTON_SUPPORT, url="https://t.me/danila_okv")]
                    ])
                )

            await asyncio.sleep(1)  # защита от спама и дерганий

        self.is_printing = False

    async def _print_file(self, file_path: str):
        """
        Отправляет файл в систему печати через lp (CUPS)
        """
        subprocess.run(["lp", file_path], check=True)


# 💡 Инициализируем глобальный экземпляр
print_manager = PrintManager(print_speed_sec_per_page=5)
