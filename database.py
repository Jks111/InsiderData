import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "insider_data.db")


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        insider TEXT NOT NULL,
        company TEXT,
        weighted_avg_price REAL,
        simulated_shares REAL,
        capital_used REAL,
        total_insider_shares INTEGER,
        created_at TEXT,
        UNIQUE(symbol, insider)
    )
    """)

    conn.commit()
    conn.close()


def insert_simulation(data: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO simulations (
        symbol,
        insider,
        company,
        weighted_avg_price,
        simulated_shares,
        capital_used,
        total_insider_shares,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["symbol"],
        data["insider"],
        data["company"],
        data["weighted_avg_price"],
        data["simulated_shares"],
        data["capital_used"],
        data["total_insider_shares"],
        datetime.utcnow().isoformat()
    ))
    
    if cursor.rowcount == 0:
        print("IGNORED:", data["symbol"], data["insider"])
    else:
        print("INSERTED:", data["symbol"], data["insider"])

    conn.commit()
    conn.close()