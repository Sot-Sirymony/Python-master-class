import sqlite3

def initialize_database():
    conn = sqlite3.connect("apartment_management.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        debts REAL DEFAULT 0.0,
        aptNo INTEGER NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Apartment (
        aptNo INTEGER PRIMARY KEY,
        status TEXT NOT NULL CHECK(status IN ('Available', 'Occupied'))
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bill (
        bill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        due_date TEXT NOT NULL,
        details TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        bill_id INTEGER,
        FOREIGN KEY (bill_id) REFERENCES Bill(bill_id)
    )
    """)
    conn.commit()
    conn.close()

