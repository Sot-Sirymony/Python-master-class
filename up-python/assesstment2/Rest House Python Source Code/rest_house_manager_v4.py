import sqlite3
from datetime import datetime


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

    def add_room(self, room_number, room_type, status='available'):
        self.conn.execute("INSERT INTO rooms (room_number, type, status) VALUES (?, ?, ?)", 
                          (room_number, room_type, status))
        self.conn.commit()

    def update_room(self, room_id, room_type):
        self.conn.execute("UPDATE rooms SET type=? WHERE id=?", (room_type, room_id))
        self.conn.commit()

    def delete_room(self, room_id):
        self.conn.execute("DELETE FROM rooms WHERE id=?", (room_id,))
        self.conn.commit()

    def add_guest(self, name, contact):
        self.conn.execute("INSERT INTO guests (name, contact) VALUES (?, ?)", (name, contact))
        self.conn.commit()

    def list_guests(self):
        cursor = self.conn.execute("SELECT id, name, contact FROM guests")
        return cursor.fetchall()

    def list_reservations(self):
        query = '''
        SELECT r.id, g.name, ro.room_number, r.check_in_date, r.check_out_date, r.status
        FROM reservations r
        JOIN guests g ON r.guest_id = g.id
        JOIN rooms ro ON r.room_id = ro.id
        '''
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def get_available_rooms(self):
        cursor = self.conn.execute("SELECT id, room_number, type, status FROM rooms WHERE status='available'")
        return cursor.fetchall()

    def delete_guest(self, guest_id):
        self.conn.execute("DELETE FROM guests WHERE id=?", (guest_id,))
        self.conn.commit()

    def delete_reservation(self, reservation_id):
        self.conn.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
        self.conn.commit()

    def log_action(self, action, details):
        with open("audit_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - {action}: {details}\n")

    def close(self):
        self.conn.close()
