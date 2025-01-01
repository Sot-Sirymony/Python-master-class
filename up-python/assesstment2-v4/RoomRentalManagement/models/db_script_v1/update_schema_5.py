import sqlite3

def update_room_table():
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()
        # Check and add tenant_id column to Room table if it doesn't exist
    cursor.execute("PRAGMA table_info(Room)")
    columns = [column[1] for column in cursor.fetchall()]  # Get column names
    if "tenant_id" not in columns:
        print("Adding tenant_id column to Room table...")
        cursor.execute("""
        ALTER TABLE Room ADD COLUMN tenant_id INTEGER REFERENCES Tenant (id) ON DELETE SET NULL;
        """)
        print("tenant_id column added successfully.")
    connection.commit()
    connection.close()

if __name__ == "__main__":
    update_room_table()
