import sqlite3
from datetime import datetime
import csv


class RestHouseManager:
    def __init__(self):
        self.conn = sqlite3.connect('rest_house.db')
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS rooms (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                room_number TEXT UNIQUE NOT NULL,
                                type TEXT NOT NULL,
                                status TEXT NOT NULL
                            )''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS guests (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                contact TEXT
                            )''')

        self.conn.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                guest_id INTEGER NOT NULL,
                                room_id INTEGER NOT NULL,
                                check_in_date TEXT NOT NULL,
                                check_out_date TEXT NOT NULL,
                                status TEXT DEFAULT 'Reserved',
                                FOREIGN KEY(guest_id) REFERENCES guests(id),
                                FOREIGN KEY(room_id) REFERENCES rooms(id)
                            )''')

    def execute_query(self, query, params=()):
        try:
            cursor = self.conn.execute(query, params)
            self.conn.commit()
            return cursor
        except sqlite3.Error as e:
            raise Exception(f"Database error: {e}")

    def add_room(self, room_number, room_type, status='available'):
        self.execute_query("INSERT INTO rooms (room_number, type, status) VALUES (?, ?, ?)", 
                           (room_number, room_type, status))

    def update_room(self, room_id, room_type):
        self.execute_query("UPDATE rooms SET type=? WHERE id=?", (room_type, room_id))

    def delete_room(self, room_id):
        self.execute_query("DELETE FROM rooms WHERE id=?", (room_id,))

    def update_room_status(self, room_id, status):
        self.execute_query("UPDATE rooms SET status=? WHERE id=?", (status, room_id))

    def add_guest(self, name, contact):
        self.execute_query("INSERT INTO guests (name, contact) VALUES (?, ?)", (name, contact))

    def list_guests(self):
        return self.execute_query("SELECT id, name, contact FROM guests").fetchall()

    def search_guests(self, query):
        query = f"%{query}%"
        return self.execute_query("SELECT id, name, contact FROM guests WHERE name LIKE ?", (query,)).fetchall()

    def list_reservations(self):
        query = '''
        SELECT r.id, g.name, ro.room_number, r.check_in_date, r.check_out_date, r.status
        FROM reservations r
        JOIN guests g ON r.guest_id = g.id
        JOIN rooms ro ON r.room_id = ro.id
        '''
        return self.execute_query(query).fetchall()
    def make_reservation(self, guest_id, room_id, check_in_date, check_out_date):
        """
        Makes a reservation by inserting a new record into the reservations table.
        Optionally, you could add checks here to ensure the room is actually available
        for the given date range before inserting.
        """

        # Check if the room is currently available
        # This step is optional but recommended:
        # Ensure the room is 'available' before making a reservation.
        room_status = self.execute_query("SELECT status FROM rooms WHERE id=?", (room_id,)).fetchone()
        if not room_status or room_status[0].lower() != 'available':
            raise Exception(f"Room ID {room_id} is not available for reservation.")

        # Insert the reservation
        self.execute_query(
            "INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date, status) VALUES (?, ?, ?, ?, 'Reserved')",
            (guest_id, room_id, check_in_date, check_out_date)
        )

        # Update the room status to 'occupied' or 'reserved' depending on your logic
        # If you'd rather mark it as 'booked' or 'reserved', choose a status that fits your application.
        self.update_room_status(room_id, 'occupied')

        # Optionally, log the action
        self.log_action("Make Reservation", f"Guest ID {guest_id} reserved Room ID {room_id} from {check_in_date} to {check_out_date}.")

    def update_reservation_status(self, reservation_id, status):
        self.execute_query("UPDATE reservations SET status=? WHERE id=?", (status, reservation_id))

    def get_available_rooms(self):
        return self.execute_query("SELECT id, room_number, type, status FROM rooms WHERE status='available'").fetchall()

    def search_rooms(self, room_type=None, status=None):
        conditions = []
        params = []
        if room_type:
            conditions.append("type=?")
            params.append(room_type)
        if status:
            conditions.append("status=?")
            params.append(status)
        query = "SELECT id, room_number, type, status FROM rooms"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        return self.execute_query(query, params).fetchall()

    def delete_guest(self, guest_id):
        self.execute_query("DELETE FROM guests WHERE id=?", (guest_id,))

    def delete_reservation(self, reservation_id):
        self.execute_query("DELETE FROM reservations WHERE id=?", (reservation_id,))

    def export_to_csv(self, table_name, file_name):
        cursor = self.conn.execute(f"SELECT * FROM {table_name}")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns)  # Write header
            writer.writerows(rows)

    def import_from_csv(self, table_name, file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            columns = next(reader)  # Read header
            placeholders = ", ".join(["?" for _ in columns])
            for row in reader:
                self.execute_query(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})", row)

    def log_action(self, action, details):
        with open("audit_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - {action}: {details}\n")

    def get_audit_logs(self):
        try:
            with open("audit_log.txt", "r") as log_file:
                return log_file.readlines()
        except FileNotFoundError:
            return []

    def close(self):
        self.conn.close()
