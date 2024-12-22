from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar
)
from rest_house_manager import RestHouseManager


class RestHouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize the database manager
        try:
            self.manager = RestHouseManager()
            self.database_status = True
        except Exception as e:
            self.database_status = False
            self.show_error(f"Database Connection Error: {e}")

        self.setWindowTitle("Rest House Management System")
        self.setGeometry(100, 100, 800, 600)

        # Status bar for database connection status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

        # Create tabbed navigation
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize tabs
        self.init_tabs()

    def init_tabs(self):
        self.add_room_tab()
        self.add_guest_tab()
        self.make_reservation_tab()
        self.check_available_rooms_tab()
        self.check_in_tab()
        self.check_out_tab()

    def update_status_bar(self):
        if self.database_status:
            self.status_bar.showMessage("Database Connected", 5000)
        else:
            self.status_bar.showMessage("Database Disconnected", 5000)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_warning(self, message):
        QMessageBox.warning(self, "Warning", message)

    def show_info(self, message):
        QMessageBox.information(self, "Info", message)

    def add_room_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        room_number_label = QLabel("Room Number:")
        self.room_number_input = QLineEdit()
        layout.addWidget(room_number_label)
        layout.addWidget(self.room_number_input)

        room_type_label = QLabel("Room Type (Single/Double/Suite):")
        self.room_type_input = QLineEdit()
        layout.addWidget(room_type_label)
        layout.addWidget(self.room_type_input)

        add_room_button = QPushButton("Add Room")
        add_room_button.clicked.connect(self.add_room)
        layout.addWidget(add_room_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Add Room")

    def add_room(self):
        room_number = self.room_number_input.text().strip()
        room_type = self.room_type_input.text().strip()
        if not room_number or not room_type:
            self.show_warning("Both Room Number and Room Type are required.")
            return

        try:
            self.manager.add_room(room_number, room_type)
            self.room_number_input.clear()
            self.room_type_input.clear()
            self.show_info(f"Room {room_number} added successfully.")
        except Exception as e:
            self.show_error(f"Error adding room: {e}")

    def add_guest_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        guest_name_label = QLabel("Guest Name:")
        self.guest_name_input = QLineEdit()
        layout.addWidget(guest_name_label)
        layout.addWidget(self.guest_name_input)

        contact_label = QLabel("Guest Contact:")
        self.contact_input = QLineEdit()
        layout.addWidget(contact_label)
        layout.addWidget(self.contact_input)

        add_guest_button = QPushButton("Add Guest")
        add_guest_button.clicked.connect(self.add_guest)
        layout.addWidget(add_guest_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Add Guest")

    def add_guest(self):
        name = self.guest_name_input.text().strip()
        contact = self.contact_input.text().strip()
        if not name or not contact:
            self.show_warning("Both Guest Name and Contact are required.")
            return

        try:
            self.manager.add_guest(name, contact)
            self.guest_name_input.clear()
            self.contact_input.clear()
            self.show_info(f"Guest {name} added successfully.")
        except Exception as e:
            self.show_error(f"Error adding guest: {e}")

    def make_reservation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        guest_id_label = QLabel("Guest ID:")
        self.guest_id_input = QLineEdit()
        layout.addWidget(guest_id_label)
        layout.addWidget(self.guest_id_input)

        room_id_label = QLabel("Room ID:")
        self.room_id_input = QLineEdit()
        layout.addWidget(room_id_label)
        layout.addWidget(self.room_id_input)

        check_in_label = QLabel("Check-In Date (YYYY-MM-DD):")
        self.check_in_input = QLineEdit()
        layout.addWidget(check_in_label)
        layout.addWidget(self.check_in_input)

        check_out_label = QLabel("Check-Out Date (YYYY-MM-DD):")
        self.check_out_input = QLineEdit()
        layout.addWidget(check_out_label)
        layout.addWidget(self.check_out_input)

        make_reservation_button = QPushButton("Make Reservation")
        make_reservation_button.clicked.connect(self.make_reservation)
        layout.addWidget(make_reservation_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Make Reservation")

    def make_reservation(self):
        guest_id = self.guest_id_input.text().strip()
        room_id = self.room_id_input.text().strip()
        check_in = self.check_in_input.text().strip()
        check_out = self.check_out_input.text().strip()

        if not (guest_id and room_id and check_in and check_out):
            self.show_warning("All fields are required to make a reservation.")
            return

        try:
            self.manager.make_reservation(guest_id, room_id, check_in, check_out)
            self.show_info(f"Reservation made for Guest ID {guest_id} in Room ID {room_id}.")
        except Exception as e:
            self.show_error(f"Error making reservation: {e}")

    def check_available_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        check_button = QPushButton("Check Available Rooms")
        check_button.clicked.connect(self.display_available_rooms)
        layout.addWidget(check_button)

        self.room_table = QTableWidget()
        self.room_table.setColumnCount(3)
        self.room_table.setHorizontalHeaderLabels(["Room ID", "Room Number", "Type"])
        layout.addWidget(self.room_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Available Rooms")

    def display_available_rooms(self):
        try:
            rooms = self.manager.get_available_rooms()
            self.room_table.setRowCount(len(rooms))
            for row_index, room in enumerate(rooms):
                for col_index, data in enumerate(room):
                    self.room_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))
        except Exception as e:
            self.show_error(f"Error fetching available rooms: {e}")

    def check_in_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        room_id_label = QLabel("Room ID:")
        self.check_in_room_id = QLineEdit()
        layout.addWidget(room_id_label)
        layout.addWidget(self.check_in_room_id)

        check_in_button = QPushButton("Check In")
        check_in_button.clicked.connect(self.check_in)
        layout.addWidget(check_in_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Check In")

    def check_in(self):
        room_id = self.check_in_room_id.text().strip()
        if not room_id:
            self.show_warning("Room ID is required for check-in.")
            return

        try:
            self.manager.check_in(room_id)
            self.show_info(f"Room {room_id} checked in successfully.")
        except Exception as e:
            self.show_error(f"Error during check-in: {e}")

    def check_out_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        room_id_label = QLabel("Room ID:")
        self.check_out_room_id = QLineEdit()
        layout.addWidget(room_id_label)
        layout.addWidget(self.check_out_room_id)

        check_out_button = QPushButton("Check Out")
        check_out_button.clicked.connect(self.check_out)
        layout.addWidget(check_out_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Check Out")

    def check_out(self):
        room_id = self.check_out_room_id.text().strip()
        if not room_id:
            self.show_warning("Room ID is required for check-out.")
            return

        try:
            self.manager.check_out(room_id)
            self.show_info(f"Room {room_id} checked out successfully.")
        except Exception as e:
            self.show_error(f"Error during check-out: {e}")

    def closeEvent(self, event):
        try:
            self.manager.close()
        except Exception as e:
            self.show_error(f"Error closing the database connection: {e}")
        event.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = RestHouseApp()
    window.show()
    app.exec()
