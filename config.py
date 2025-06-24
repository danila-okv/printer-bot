import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_IDS = set(map(int, os.getenv("ADMIN_IDS", "").split(",")))
