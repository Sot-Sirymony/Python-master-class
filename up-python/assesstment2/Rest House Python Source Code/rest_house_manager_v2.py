import sqlite3

class RestHouseManager:
    def __init__(self):
        self.conn = sqlite3.connect('rest_house.db')
        self.create_tables()

    def create_tables(self):
        # Create rooms table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS rooms (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                room_number TEXT UNIQUE NOT NULL,
                                type TEXT NOT NULL,
                                status TEXT NOT NULL
                            )''')

        # Create guests table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS guests (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                contact TEXT
                            )''')

        # Create reservations table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                guest_id INTEGER NOT NULL,
                                room_id INTEGER NOT NULL,
                                check_in_date TEXT NOT NULL,
                                check_out_date TEXT NOT NULL,
                                FOREIGN KEY(guest_id) REFERENCES guests(id),
                                FOREIGN KEY(room_id) REFERENCES rooms(id)
                            )''')

    def add_room(self, room_number, room_type, status='available'):
        self.conn.execute("INSERT INTO rooms (room_number, type, status) VALUES (?, ?, ?)", 
                          (room_number, room_type, status))
        self.conn.commit()

    def add_guest(self, name, contact):
        self.conn.execute("INSERT INTO guests (name, contact) VALUES (?, ?)", (name, contact))
        self.conn.commit()

    def list_guests(self):
        """
        Retrieves all guests from the database.
        Returns a list of tuples, each containing (id, name, contact).
        """
        cursor = self.conn.execute("SELECT id, name, contact FROM guests")
        return cursor.fetchall()

    def make_reservation(self, guest_id, room_id, check_in, check_out):
        self.conn.execute("INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date) VALUES (?, ?, ?, ?)",
                          (guest_id, room_id, check_in, check_out))
        self.conn.commit()

    def get_available_rooms(self):
        cursor = self.conn.execute("SELECT * FROM rooms WHERE status='available'")
        return cursor.fetchall()

    def check_in(self, room_id):
        self.conn.execute("UPDATE rooms SET status='occupied' WHERE id=?", (room_id,))
        self.conn.commit()

    def check_out(self, room_id):
        self.conn.execute("UPDATE rooms SET status='available' WHERE id=?", (room_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
