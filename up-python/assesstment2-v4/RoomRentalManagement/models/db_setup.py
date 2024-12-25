import sqlite3

def initialize_db():
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Property (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        address TEXT,
        description TEXT,
        amenities TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT,
        size REAL,
        rental_price REAL,
        occupancy_status TEXT DEFAULT 'available',
        FOREIGN KEY (property_id) REFERENCES Property (id) ON DELETE CASCADE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tenant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        method TEXT,
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id),
        FOREIGN KEY (room_id) REFERENCES Room (id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lease (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tenant_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        status TEXT DEFAULT 'active',
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id),
        FOREIGN KEY (room_id) REFERENCES Room (id)
    );
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_db()
