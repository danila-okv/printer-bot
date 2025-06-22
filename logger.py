import os
from datetime import datetime

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def log(user_id: int, handler: str, user_input: str = "", extra: str = ""):
    today = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%H:%M")
    log_file = os.path.join(LOG_DIR, f"{today}.log")

    line = f"[{timestamp}] {user_id}: {handler}"
    if extra:
        line += f" | {extra}"
    if user_input:
        line += f" : {user_input}"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
