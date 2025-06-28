# modules/printing/print_job.py

import asyncio
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from aiogram import Bot
from modules.ui.messages import PRINT_DONE_TEXT
from modules.ui.keyboards import print_done_kb, print_error_kb
from modules.analytics.logger import info, error
from db import get_connection


@dataclass
class PrintJob:
    user_id: int
    file_path: str
    file_name: str
    bot: Bot
    pages: int = 0
    duplex: bool = False
    layout: str = ""         # например "9-up"
    page_ranges: str = ""    # например "1,3-5"

    async def run(self):
        job_id = None
        try:
            # Формируем команду
            cmd = ["lp"]
            if self.duplex:
                cmd += ["-o", "sides=two-sided-long-edge"]
            if self.layout:
                cmd += ["-o", f"number-up={self.layout}"]
            if self.page_ranges:
                cmd += ["-P", self.page_ranges]
            cmd.append(self.file_path)

            # Запускаем печать
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"lp error: {result.stderr.strip()}")

            job_id_str = result.stdout.strip()
            info(self.user_id, "print_job", f"Job started {self.file_name}: {job_id_str}")

            # Извлекаем job_id из lp ответа
            if "-" in job_id_str:
                job_id = job_id_str.split("-")[1].split()[0]

            # Сохраняем job в БД
            self.save_to_db(status="queued", job_id=job_id)

            # Ждём завершения
            while True:
                lpstat = subprocess.run(["lpstat", "-W", "not-completed"], capture_output=True, text=True)
                if job_id and job_id not in lpstat.stdout:
                    break
                await asyncio.sleep(3)

            # Завершено
            info(self.user_id, "print_job", f"Printing ended: {self.file_name}")
            self.update_status("done")
            await self.bot.send_message(
                chat_id=self.user_id,
                text=PRINT_DONE_TEXT,
                reply_markup=print_done_kb
            )

        except Exception as e:
            error(self.user_id, "print_job", f"Printing error: {e}")
            self.update_status("error")
            await self.bot.send_message(
                chat_id=self.user_id,
                text=f"❌ Ошибка при печати файла «{self.file_name}». Попробуйте позже.",
                reply_markup=print_error_kb
            )

    def save_to_db(self, status: str = "queued", job_id: str | None = None):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO print_jobs (
                    user_id, file_name, pages, duplex, layout,
                    page_ranges, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.user_id, self.file_name, self.pages,
                int(self.duplex), self.layout, self.page_ranges,
                status, datetime.now()
            ))
            conn.commit()

    def update_status(self, status: str):
        with get_connection() as conn:
            conn.execute("""
                UPDATE print_jobs
                SET status = ?, completed_at = ?
                WHERE user_id = ? AND file_name = ? AND status != 'done'
            """, (
                status, datetime.now(), self.user_id, self.file_name
            ))
            conn.commit()


def add_job(job: PrintJob):
    asyncio.create_task(job.run())
