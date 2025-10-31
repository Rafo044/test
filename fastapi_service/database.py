"""
Database modulu FastAPI servisində datanı sqlite3 də saxlamaga kömək edir.
"""

import sqlite3

import os

from dotenv import load_dotenv


load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH")


def create_tables():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS supermarket (
        Invoice_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Branch TEXT,
        City TEXT,
        Customer_type TEXT,
        Gender TEXT,
        Product_line TEXT,
        Unit_price REAL,
        Quantity INTEGER,
        Payment TEXT
    )
    """)
    conn.commit()
    return conn
