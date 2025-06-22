import asyncio
import os
import subprocess
from dataclasses import dataclass
from collections import deque
from aiogram import Bot
from print_job import PrintJob
from messages import *
from keyboards import print_done_keyboard
from handlers.notifier import notify_print_complete

# Очередь и управление
print_queue = deque()
processing = False
lock = asyncio.Lock()

async def print_worker():
    global processing

    async with lock:
        if processing or not print_queue:
            return
        processing = True

    while print_queue:
        job = print_queue.popleft()
        position = len(print_queue) + 1
        try:
            if position > 1:
                await job.bot.send_message(
                    chat_id=job.user_id,
                    text=f"📄 Файл {job.file_name} поставлен в очередь на печать. Позиция в очереди: {position}"
                )
            else:
                await job.bot.send_message(
                    chat_id=job.user_id,
                    text=PRINT_START_TEXT.format(file_name=job.file_name)
                )
            await job.run()
        except Exception as e:
            print(f"[ERROR] Ошибка выполнения задания печати: {e}")
        await asyncio.sleep(1)

    processing = False

def add_job(job: PrintJob):
    print_queue.append(job)
    asyncio.create_task(print_worker())