# modules/printing/print_job.py

import asyncio
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from aiogram import Bot
from modules.ui.messages import PRINT_DONE_TEXT
from modules.ui.keyboards.print import print_done_kb, print_error_kb
from modules.ui.keyboards.tracker import send_managed_message
from modules.analytics.logger import info, error
from db import get_connection


@dataclass
class PrintJob:
    user_id: int
    file_path: str
    file_name: str
    bot: Bot
    page_count: int = 0
    duplex: bool = False
    layout: str = "1"
    pages: str = ""    # например "1,3-5"
    copies: int = 1

    async def run(self):
        job_id = None
        try:
            # Формируем команду
            cmd = ["lp"]
            if self.duplex:
                cmd += ["-o", "sides=two-sided-long-edge"]
            else:
                cmd += ["-o", "sides=one-sided"]
            if self.layout:
                cmd += ["-o", f"number-up={self.layout}"]
            if self.pages:
                cmd += ["-P", self.pages]
            if self.copies > 1:
                cmd += ["-n", str(self.copies)]
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
            await send_managed_message(
                self.bot,
                self.user_id,
                PRINT_DONE_TEXT,
                print_done_kb
            )
        except Exception as e:
            error(self.user_id, "print_job", f"Printing error: {e}")
            self.update_status("error")
            await send_managed_message(
                self.bot,
                self.user_id,
                f"❌ Ошибка при печати файла «{self.file_name}». Попробуйте позже.",
                print_error_kb
            )

    def save_to_db(self, status: str = "queued", job_id: str | None = None):
        with get_connection() as conn:
            conn.execute("""
                INSERT INTO print_jobs (
                    user_id, file_name, page_count, duplex, layout,
                    pages, copies, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.user_id, self.file_name, self.page_count,
                int(self.duplex), self.layout, self.pages, self.copies,
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
