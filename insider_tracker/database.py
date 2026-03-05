import sqlite3
from datetime import datetime
import os
from datetime import datetime

snapshot_date = datetime.utcnow().date().isoformat()




"""
    INSERT OR IGNORE INTO simulations
    
    Each column represents a specific part of the insider signal and its
    simulated performance.

    Columns explained:

    - symbol:
        The stock ticker symbol (e.g., AAPL, KKR).
        Identifies the traded company in the market.

    - insider:
        Name of the insider who executed the trade.
        Used together with symbol to uniquely identify an insider signal.

    - company:
        Full company name for readability and reporting.

    - weighted_avg_price:
        The weighted average purchase price calculated from all grouped
        insider buy trades.
        Formula:
            total_amount / total_shares
        Represents the insider's effective cost basis.

    - simulated_shares:
        Number of shares bought with fixed capital (e.g., €1000).
        Formula:
            capital / weighted_avg_price
        Allows comparison across different stocks regardless of price level.

    - capital_used:
        The fixed simulation investment amount (e.g., €1000).
        Makes performance comparable across all signals.

    - total_insider_shares:
        Total number of shares purchased by the insider across grouped trades.

    - current_price:
        Latest market price fetched via yfinance at runtime.
        Used to evaluate current performance of the insider signal.

    - current_value:
        Current value of the simulated investment.
        Formula:
            simulated_shares * current_price

    - profit:
        Absolute gain or loss in currency.
        Formula:
            current_value - capital_used

    - return_pct:
        Percentage return of the simulated investment.
        Formula:
            (profit / capital_used) * 100
        This is the key performance metric.

    - created_at:
        UTC timestamp when this simulation snapshot was stored.
        Useful for tracking performance history over time.

    UNIQUE(symbol, insider):
        Ensures only one active record per insider per stock.
        Prevents duplicate inserts when the pipeline runs multiple times.
"""





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
        total_insider_shares REAL,
        current_price REAL,
        currency TEXT,
        current_value REAL,
        profit REAL,
        return_pct REAL,
        snapshot_date TEXT NOT NULL,
        created_at TEXT,
        UNIQUE(symbol, insider, snapshot_date)
)
    """)

    conn.commit()
    conn.close()
    
def insert_simulation(data: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    snapshot_date = datetime.utcnow().date().isoformat()
    created_at = datetime.utcnow().isoformat()

    cursor.execute("""
    INSERT OR IGNORE INTO simulations (
        symbol,
        insider,
        company,
        weighted_avg_price,
        simulated_shares,
        capital_used,
        total_insider_shares,
        current_price,
        currency,
        current_value,
        profit,
        return_pct,
        snapshot_date,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["symbol"],
        data["insider"],
        data["company"],
        data["weighted_avg_price"],
        data["simulated_shares"],
        data["capital_used"],
        data["total_insider_shares"],
        data["current_price"],
        data["currency"],
        data["current_value"],
        data["profit"],
        data["return_pct"],
        snapshot_date,
        created_at
    ))

    
    if cursor.rowcount == 0:
        print("IGNORED:", data["symbol"], data["insider"])
    else:
        print("INSERTED:", data["symbol"], data["insider"])

    conn.commit()
    conn.close()