import sqlite3

def update_room_table():
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()

    # Check existing columns in the Room table
    cursor.execute("PRAGMA table_info(Room);")
    columns = [col[1] for col in cursor.fetchall()]

    # Add missing columns if not already present
    if 'payment_frequency' not in columns:
        cursor.execute("ALTER TABLE Room ADD COLUMN payment_frequency TEXT;")
    if 'security_deposit' not in columns:
        cursor.execute("ALTER TABLE Room ADD COLUMN security_deposit REAL;")
    if 'grace_period' not in columns:
        cursor.execute("ALTER TABLE Room ADD COLUMN grace_period INTEGER;")
    if 'rental_price' not in columns:
        cursor.execute("ALTER TABLE Room ADD COLUMN rental_price REAL;")
    if 'occupancy_status' not in columns:
        cursor.execute("ALTER TABLE Room ADD COLUMN occupancy_status TEXT DEFAULT 'Available';")

    connection.commit()
    connection.close()

if __name__ == "__main__":
    update_room_table()
