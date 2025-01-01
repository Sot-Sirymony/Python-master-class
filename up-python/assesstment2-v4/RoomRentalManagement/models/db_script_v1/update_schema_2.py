import sqlite3

connection = sqlite3.connect('rental_management.db')
cursor = connection.cursor()

try:
    cursor.execute("ALTER TABLE Room ADD COLUMN amenities TEXT;")
    connection.commit()
    print("Column 'amenities' added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
finally:
    connection.close()
