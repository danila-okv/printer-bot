import asyncio
import os
import subprocess
from dataclasses import dataclass
from aiogram import Bot
from messages import PRINT_DONE_TEXT
from keyboards import print_done_keyboard, print_error_keyboard

@dataclass
class PrintJob:
    user_id: int
    file_path: str
    file_name: str
    bot: Bot

    async def run(self):
        try:
            # Отправляем файл в печать через lp и получаем job-id
            result = subprocess.run(["lp", self.file_path], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"lp error: {result.stderr.strip()}")

            print_id_line = result.stdout.strip()  # e.g. "request id is HP_Printer-65 (1 file(s))"
            print(f"[DEBUG] Печать запущена: {print_id_line}")

            job_id = None
            if "-" in print_id_line:
                job_id = print_id_line.split("-")[1].split()[0]

            if not job_id:
                raise RuntimeError("Не удалось извлечь job-id из ответа lp")

            # Проверяем статус печати каждые 3 секунды, без ограничения по попыткам
            while True:
                lpstat = subprocess.run(["lpstat", "-W", "not-completed"], capture_output=True, text=True)
                if job_id not in lpstat.stdout:
                    break
                print(f"[DEBUG] Печать {job_id} ещё не завершена. Ожидание...")
                await asyncio.sleep(3)

            await self.bot.send_message(
                chat_id=self.user_id,
                text=PRINT_DONE_TEXT,
                reply_markup=print_done_keyboard
            )
        except Exception as e:
            print(f"[ERROR] Ошибка при печати: {e}")
            await self.bot.send_message(
                chat_id=self.user_id,
                text=f"❌ Ошибка при печати файла «{self.file_name}». Попробуйте позже.",
                reply_markup=print_error_keyboard
            )

def add_job(job: PrintJob):
    asyncio.create_task(job.run())
