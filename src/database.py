import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "transactions.db"

def get_connection():

    conn = sqlite3.connect(DB_PATH)
    
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            date        TEXT NOT NULL,
            description TEXT NOT NULL,
            amount      REAL NOT NULL,
            currency    TEXT NOT NULL,
            category    TEXT,
            confidence  TEXT,
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")

def save_transaction(date, description, amount, currency, category, confidence):
    
    conn = get_connection()
    conn.execute("""
        INSERT INTO transactions (date, description, amount, currency, category, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, description, amount, currency, category, confidence))
    conn.commit()
    conn.close()

def get_all_transactions():
    
    conn = get_connection()
    rows = conn.execute("SELECT * FROM transactions ORDER BY date").fetchall()
    conn.close()
    return rows

def get_summary_by_category():
    
    conn = get_connection()
    rows = conn.execute("""
        SELECT 
            category,
            COUNT(*)        AS total_transacciones,
            SUM(amount)     AS gasto_total,
            AVG(amount)     AS gasto_promedio
        FROM transactions
        GROUP BY category
        ORDER BY gasto_total DESC
    """).fetchall()
    conn.close()
    return rows