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

        # Баны
        c.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            user_id     INTEGER PRIMARY KEY,
            reason      TEXT,
            banned_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Задания на печать
        c.execute("""
        CREATE TABLE IF NOT EXISTS print_jobs (
            job_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       INTEGER NOT NULL,
            file_name     TEXT,
            pages         INTEGER NOT NULL,
            duplex        INTEGER DEFAULT 0,        -- 0 = односторонняя, 1 = двухсторонняя
            layout        TEXT,                     -- например "9-up"
            page_ranges   TEXT,                     -- например "1,2-5,10"
            status        TEXT NOT NULL,            -- queued, printing, done, error
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at    TIMESTAMP,
            completed_at  TIMESTAMP
            -- без FOREIGN KEY, просто хранить user_id
        );
        """)

        # Состояние бота (pause/resume и другие флаги)
        c.execute("""
        CREATE TABLE IF NOT EXISTS bot_state (
            key   TEXT PRIMARY KEY,
            value TEXT
        );
        """)

        # Очередь действий, совершённых во время паузы
        c.execute("""
        CREATE TABLE IF NOT EXISTS paused_actions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            action      TEXT NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Промо-акции
        c.execute("""
        CREATE TABLE IF NOT EXISTS promos (
            code                TEXT PRIMARY KEY,
            activations_total   INTEGER NOT NULL,
            activations_used    INTEGER NOT NULL DEFAULT 0,
            reward_type         TEXT NOT NULL,    -- 'pages' или 'discount'
            reward_value        REAL NOT NULL,
            created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at          TIMESTAMP
        );
        """)

        # Бонусные (бесплатные) страницы у пользователей
        c.execute("""
        CREATE TABLE IF NOT EXISTS user_bonus (
            user_id     INTEGER PRIMARY KEY,
            bonus_pages INTEGER NOT NULL DEFAULT 0
        );
        """)

        # Расходы на расходники
        c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            amount      REAL NOT NULL,
            description TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        conn.commit()
