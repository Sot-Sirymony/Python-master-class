import sqlite3

def add_tenant(first_name, last_name, phone, email):
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO Tenant (first_name, last_name, phone, email)
    VALUES (?, ?, ?, ?)
    """, (first_name, last_name, phone, email))
    connection.commit()
    connection.close()

def get_all_tenants():
    connection = sqlite3.connect('rental_management.db')
    cursor = connection.cursor()
    cursor.execute("SELECT first_name || ' ' || last_name AS name, phone, email FROM Tenant")
    tenants = [{"name": row[0], "phone": row[1], "email": row[2]} for row in cursor.fetchall()]
    connection.close()
    return tenants
