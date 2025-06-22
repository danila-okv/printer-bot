import os
import json

BANLIST_FILE = "data/banlist.json"

def _load_banlist():
    if not os.path.exists(BANLIST_FILE):
        return set()
    with open(BANLIST_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def _save_banlist(banned_ids):
    with open(BANLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(list(banned_ids), f, indent=2)

def is_banned(user_id: int) -> bool:
    return user_id in _load_banlist()

def ban_user(user_id: int):
    banned = _load_banlist()
    banned.add(user_id)
    _save_banlist(banned)

def unban_user(user_id: int):
    banned = _load_banlist()
    banned.discard(user_id)
    _save_banlist(banned)
