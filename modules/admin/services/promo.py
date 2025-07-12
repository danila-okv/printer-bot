from db import get_connection
from datetime import datetime, timedelta

def create_promo(code: str, activations_total: int, reward_type: str, reward_value: float, expires_at: str | None = None):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO promos (code, activations_total, reward_type, reward_value, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (code, activations_total, reward_type, reward_value, expires_at))
        conn.commit()

def list_promos() -> list[dict]:
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT code, activations_total, activations_used, reward_type, reward_value, expires_at
            FROM promos
            ORDER BY created_at DESC
        """)
        return [dict(row) for row in cur.fetchall()]

def get_promo_details(code: str) -> dict | None:
    with get_connection() as conn:
        cur = conn.execute("""
            SELECT code, activations_total, activations_used, reward_type, reward_value, created_at, expires_at
            FROM promos
            WHERE code = ?
        """, (code,))
        row = cur.fetchone()
        return dict(row) if row else None

def promo_exists(code: str) -> bool:
    with get_connection() as conn:
        cur = conn.execute("SELECT 1 FROM promos WHERE code = ?", (code,))
        return cur.fetchone() is not None