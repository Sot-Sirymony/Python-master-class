import sqlite3

class RestHouseManager:
    def __init__(self):
        self.conn = sqlite3.connect('rest_house.db')
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS rooms (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                room_number TEXT UNIQUE NOT NULL,
                                type TEXT NOT NULL,
                                status TEXT NOT NULL CHECK(status IN ('available', 'occupied', 'maintenance')),
                                is_active INTEGER DEFAULT 1
                            )''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS guests (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                contact TEXT,
                                is_active INTEGER DEFAULT 1
                            )''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                guest_id INTEGER NOT NULL,
                                room_id INTEGER NOT NULL,
                                check_in_date TEXT NOT NULL,
                                check_out_date TEXT NOT NULL,
                                status TEXT NOT NULL CHECK(status IN ('reserved', 'completed', 'canceled')),
                                FOREIGN KEY(guest_id) REFERENCES guests(id),
                                FOREIGN KEY(room_id) REFERENCES rooms(id)
                            )''')

    # Room Management
    def add_room(self, room_number, room_type):
        self.conn.execute("INSERT INTO rooms (room_number, type, status) VALUES (?, ?, 'available')", (room_number, room_type))
        self.conn.commit()

    def get_all_rooms(self):
        return self.conn.execute("SELECT id, room_number, type, status FROM rooms WHERE is_active=1").fetchall()

    def update_room(self, room_id, room_type, status):
        self.conn.execute("UPDATE rooms SET type=?, status=? WHERE id=?", (room_type, status, room_id))
        self.conn.commit()

    def delete_room(self, room_id):
        self.conn.execute("UPDATE rooms SET is_active=0 WHERE id=?", (room_id,))
        self.conn.commit()

    def get_available_rooms(self):
        return self.conn.execute("SELECT id, room_number, type, status FROM rooms WHERE status='available' AND is_active=1").fetchall()

    # Guest Management
    def get_all_guests(self):
        return self.conn.execute("SELECT id, name, contact FROM guests WHERE is_active=1").fetchall()

    def delete_guest(self, guest_id):
        active_reservations = self.conn.execute(
            "SELECT COUNT(*) FROM reservations WHERE guest_id=? AND status='reserved'", (guest_id,)
        ).fetchone()[0]
        if active_reservations > 0:
            raise Exception("Cannot delete guest with active reservations.")
        self.conn.execute("UPDATE guests SET is_active=0 WHERE id=?", (guest_id,))
        self.conn.commit()

    # Reservation Management
    def add_reservation(self, guest_id, room_id, check_in, check_out):
        self.conn.execute("INSERT INTO reservations (guest_id, room_id, check_in_date, check_out_date, status) VALUES (?, ?, ?, ?, 'reserved')",
                          (guest_id, room_id, check_in, check_out))
        self.conn.execute("UPDATE rooms SET status='occupied' WHERE id=?", (room_id,))
        self.conn.commit()

    def get_all_reservations(self):
        return self.conn.execute("SELECT r.id, g.name, ro.room_number, r.check_in_date, r.check_out_date, r.status "
                                 "FROM reservations r "
                                 "JOIN guests g ON r.guest_id = g.id "
                                 "JOIN rooms ro ON r.room_id = ro.id").fetchall()

    def delete_reservation(self, reservation_id, room_id):
        self.conn.execute("UPDATE rooms SET status='available' WHERE id=?", (room_id,))
        self.conn.execute("DELETE FROM reservations WHERE id=?", (reservation_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
