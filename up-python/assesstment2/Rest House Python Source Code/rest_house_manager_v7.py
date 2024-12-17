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

    # CRUD methods
    def add_room(self, room_number, room_type, status='available'):
        self.conn.execute("INSERT INTO rooms (room_number, type, status) VALUES (?, ?, ?)", 
                          (room_number, room_type, status))
        self.conn.commit()

    def add_guest(self, name, contact):
        self.conn.execute("INSERT INTO guests (name, contact) VALUES (?, ?)", (name, contact))
        self.conn.commit()

    def make_reservation(self, guest_id, room_id, check_in, check_out):
        self.conn.execute("INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date) VALUES (?, ?, ?, ?)",
                          (guest_id, room_id, check_in, check_out))
        self.check_in(room_id)
        self.conn.commit()

    # Additional methods
    def delete_guest(self, guest_id):
        self.conn.execute("DELETE FROM reservations WHERE guest_id=?", (guest_id,))
        self.conn.execute("DELETE FROM guests WHERE id=?", (guest_id,))
        self.conn.commit()

    def delete_reservation(self, reservation_id):
        room_id = self.conn.execute("SELECT room_id FROM reservations WHERE id=?", (reservation_id,)).fetchone()
        if room_id:
            self.check_out(room_id[0])
        self.conn.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
        self.conn.commit()

    def update_room_status(self, room_id, status):
        self.conn.execute("UPDATE rooms SET status=? WHERE id=?", (status, room_id))
        self.conn.commit()

    def check_in(self, room_id):
        self.update_room_status(room_id, 'occupied')

    def check_out(self, room_id):
        self.update_room_status(room_id, 'available')

    def get_available_rooms(self):
        cursor = self.conn.execute("SELECT * FROM rooms WHERE status='available'")
        return cursor.fetchall()

    def get_occupied_rooms(self):
        cursor = self.conn.execute("SELECT * FROM rooms WHERE status='occupied'")
        return cursor.fetchall()

    def get_room_details(self, room_id):
        cursor = self.conn.execute("SELECT * FROM rooms WHERE id=?", (room_id,))
        return cursor.fetchone()

    def list_guests(self):
        return self.conn.execute("SELECT * FROM guests").fetchall()

    def list_reservations(self):
        query = '''SELECT r.id, g.name AS guest_name, rm.room_number, r.check_in_date, r.check_out_date
                   FROM reservations r
                   JOIN guests g ON r.guest_id = g.id
                   JOIN rooms rm ON r.room_id = rm.id'''
        return self.conn.execute(query).fetchall()

    def close(self):
        self.conn.close()
