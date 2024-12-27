# File: controllers/rental_management_controller.py
from sqlite3 import connect

def set_rental_price_and_terms(room_id, rental_price, payment_frequency, security_deposit, grace_period):
    connection = connect('rental_management.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET rental_price = ?,
            payment_frequency = ?,
            security_deposit = ?,
            grace_period = ?
        WHERE id = ?
        """, (rental_price, payment_frequency, security_deposit, grace_period, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error setting rental terms: {e}")
    finally:
        connection.close()
        
def update_tenant_for_room(room_id, tenant_id):
    connection = connect('rental_management.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET tenant_id = ?
        WHERE id = ?
        """, (tenant_id, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating tenant for room: {e}")
        raise
    finally:
        connection.close()          

def update_occupancy_status(room_id, status):
    connection = connect('rental_management.db')
    cursor = connection.cursor()
    try:
        cursor.execute("""
        UPDATE Room
        SET occupancy_status = ?
        WHERE id = ?
        """, (status, room_id))
        connection.commit()
    except Exception as e:
        print(f"Error updating occupancy status: {e}")
    finally:
        connection.close()

# def fetch_room_details():
#     connection = connect('rental_management.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         SELECT id, name, type, rental_price, payment_frequency, security_deposit, grace_period, occupancy_status
#         FROM Room
#         """)
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching room details: {e}")
#         return []
#     finally:
#         connection.close()
# def fetch_room_details():
#     connection = connect('rental_management.db')
#     cursor = connection.cursor()
#     try:
#         cursor.execute("""
#         SELECT 
#             Room.id, Room.name, Room.type, Room.rental_price, Room.payment_frequency,
#             Room.security_deposit, Room.grace_period, Room.occupancy_status,
#             Tenant.first_name || ' ' || Tenant.last_name AS tenant_name
#         FROM Room
#         LEFT JOIN Tenant ON Room.tenant_id = Tenant.id
#         """)
#         return cursor.fetchall()
#     except Exception as e:
#         print(f"Error fetching room details: {e}")
#         return []
#     finally:
#         connection.close()
def fetch_room_details():
    connection = connect('rental_management.db')
    cursor = connection.cursor()
    try:
        # Query to fetch room details along with tenant information
        cursor.execute("""
        SELECT 
            Room.id, 
            Room.name, 
            Room.type, 
            Room.rental_price, 
            Room.payment_frequency,
            Room.security_deposit, 
            Room.grace_period, 
            Room.occupancy_status,
            COALESCE(Tenant.first_name || ' ' || Tenant.last_name, 'No Tenant') AS tenant_name
        FROM Room
        LEFT JOIN Tenant ON Room.tenant_id = Tenant.id
        """)
        # Fetch and return all rows
        return cursor.fetchall()
    except Exception as e:
        # Print error details for debugging
        print(f"Error fetching room details: {e}")
        return []
    finally:
        # Ensure the database connection is closed
        connection.close()
