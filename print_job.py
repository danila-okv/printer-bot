import asyncio
import os
import subprocess
from dataclasses import dataclass
from aiogram import Bot
from messages import PRINT_DONE_TEXT
from keyboards import print_done_keyboard, print_error_keyboard
from logger import log

@dataclass
class PrintJob:
    user_id: int
    file_path: str
    file_name: str
    bot: Bot

    async def run(self):
        try:
            # Отправляем файл в печать через lp и получаем job-id
            result = subprocess.run(["lp", "-o", "ColorModel=Mono", self.file_path], capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"lp error: {result.stderr.strip()}")

            print_id_line = result.stdout.strip()  # e.g. "request id is HP_Printer-65 (1 file(s))"
            log(self.user_id, f"Start file printing: {self.file_name}, lp output: {print_id_line}")

            job_id = None
            if "-" in print_id_line:
                job_id = print_id_line.split("-")[1].split()[0]

            if not job_id:
                log(self.user_id, f"Failed to extract job-id from lp output: {print_id_line}")
                raise RuntimeError(f"Failed to extract job-id from lp output: {print_id_line}")

            # Check if the job is in progress every 3 seconds
            while True:
                lpstat = subprocess.run(["lpstat", "-W", "not-completed"], capture_output=True, text=True)
                if job_id not in lpstat.stdout:
                    break
                log(self.user_id, f"Print job {job_id} still in progress for file {self.file_name}")
                await asyncio.sleep(3)

            log(self.user_id, f"Print job {job_id} completed for file {self.file_name}")
            await self.bot.send_message(
                chat_id=self.user_id,
                text=PRINT_DONE_TEXT,
                reply_markup=print_done_keyboard
            )
        except Exception as e:
            log(self.user_id, f"Print error: {e}")
            await self.bot.send_message(
                chat_id=self.user_id,
                text=f"❌ Ошибка при печати файла «{self.file_name}». Попробуйте позже.",
                reply_markup=print_error_keyboard
            )

def add_job(job: PrintJob):
    asyncio.create_task(job.run())
