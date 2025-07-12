# db.py
import sqlite3
from config import DB_PATH

def get_connection():
    """
    Открывает соединение с SQLite БД.
    """
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    # Включаем проверку внешних ключей, если потребуется:
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """
    Создаёт все необходимые таблицы, если их ещё нет.
    """
    with get_connection() as conn:
        c = conn.cursor()

        # Banlist
        c.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            user_id     INTEGER PRIMARY KEY,
            reason      TEXT,
            banned_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Print job
        c.execute("""
        CREATE TABLE IF NOT EXISTS print_jobs (
            job_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            file_name     TEXT,
            page_count    INTEGER NOT NULL,
            duplex        INTEGER DEFAULT 0,        -- 0 = односторонняя, 1 = двухсторонняя
            layout        TEXT,                     -- например "9-up"
            pages         TEXT,                     -- например "1,2-5,10"
            copies        INTEGER DEFAULT 1,        -- количество копий
            status        TEXT NOT NULL,            -- queued, printing, done, error
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at    TIMESTAMP,
            completed_at  TIMESTAMP
            -- без FOREIGN KEY, просто хранить user_id
        );
        """)

        # Bot state (pause/resume)
        c.execute("""
        CREATE TABLE IF NOT EXISTS bot_state (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
        """)

        # Queue after /pause
        c.execute("""
        CREATE TABLE IF NOT EXISTS paused_actions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            action      TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Promo
        c.execute("""
        CREATE TABLE IF NOT EXISTS promos (
            code                TEXT PRIMARY KEY,
            activations_total   INTEGER NOT NULL,
            activations_used    INTEGER NOT NULL DEFAULT 0,
            reward_type         TEXT NOT NULL CHECK(reward_type IN ('pages', 'discount')),
            reward_value        REAL NOT NULL,        -- count of pages or discount percentage
            created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at          TIMESTAMP,            -- expiration date
            duration_days       INTEGER               -- if promo is time-limited
        );
        """)


        # Promo activations
        c.execute("""
        CREATE TABLE IF NOT EXISTS promo_activations (
            user_id         INTEGER NOT NULL,
            code            TEXT NOT NULL,
            activated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, code)
        );
        """)

        # Bonuses
        c.execute("""
        CREATE TABLE IF NOT EXISTS user_bonus (
            user_id     INTEGER PRIMARY KEY,
            bonus_pages INTEGER NOT NULL DEFAULT 0
        );
        """)

        # Expenses
        c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL NOT NULL,
            description TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Active inline-keyboards
        c.execute("""
        CREATE TABLE IF NOT EXISTS active_keyboards (
            user_id     INTEGER PRIMARY KEY,
            message_id  INTEGER NOT NULL
        );
        """)

        conn.commit()
