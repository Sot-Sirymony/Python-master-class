## Step 1: Database Setup
# Add columns and tables to support rental prices, terms, and occupancy tracking.

import sqlite3

def initialize_rental_management_db():
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()

    # Update Room table with rental-related fields
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Room (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        type TEXT,
        size REAL,
        rental_price REAL,
        payment_frequency TEXT,
        security_deposit REAL,
        grace_period INTEGER,
        occupancy_status TEXT DEFAULT 'Available',
        FOREIGN KEY (property_id) REFERENCES Property (id) ON DELETE CASCADE
    );
    """)

    # Create Lease Agreements Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Lease (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        tenant_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY (room_id) REFERENCES Room (id),
        FOREIGN KEY (tenant_id) REFERENCES Tenant (id)
    );
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_rental_management_db()