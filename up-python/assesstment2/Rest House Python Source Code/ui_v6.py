from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar, QHeaderView
)
from PyQt6.QtCore import Qt
from rest_house_manager_v2 import RestHouseManager
import csv
import re


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

        # Apply theme and style
        self.apply_theme()

        # Create tabbed navigation
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize tabs
        self.init_tabs()

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50; 
                color: white; 
                border: none; 
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
        """)

    def init_tabs(self):
        self.add_guest_tab()
        self.list_guests_tab()
        self.make_reservation_tab()
        self.reservation_overview_tab()
        self.check_available_rooms_tab()

    def update_status_bar(self):
        if self.database_status:
            self.status_bar.showMessage("Database Connected", 5000)
        else:
            self.status_bar.showMessage("Database Disconnected", 5000)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Info", message)

    def is_valid_date(self, date_str):
        pattern = r"^\d{4}-\d{2}-\d{2}$"  # YYYY-MM-DD format
        return re.match(pattern, date_str) is not None

    # Add Guest Tab
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
            self.show_error("Both Guest Name and Contact are required.")
            return

        try:
            self.manager.add_guest(name, contact)
            self.guest_name_input.clear()
            self.contact_input.clear()
            self.show_info(f"Guest {name} added successfully.")
        except Exception as e:
            self.show_error(f"Error adding guest: {e}")

    # List Guests Tab with Search and Delete
    def list_guests_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.guest_search_input = QLineEdit()
        self.guest_search_input.setPlaceholderText("Search Guests...")
        self.guest_search_input.textChanged.connect(self.search_guests)
        layout.addWidget(self.guest_search_input)

        self.guest_table = QTableWidget()
        self.guest_table.setColumnCount(2)
        self.guest_table.setHorizontalHeaderLabels(["Guest ID", "Guest Name"])
        self.guest_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.guest_table)

        refresh_button = QPushButton("Refresh Guests")
        refresh_button.clicked.connect(self.display_guests)
        layout.addWidget(refresh_button)

        delete_button = QPushButton("Delete Selected Guest")
        delete_button.clicked.connect(self.delete_selected_guest)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "List Guests")

    def display_guests(self):
        guests = self.manager.list_guests()
        self.update_guest_table(guests)

    def update_guest_table(self, guests):
        self.guest_table.setRowCount(len(guests))
        for row_index, guest in enumerate(guests):
            for col_index, data in enumerate(guest):
                self.guest_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def search_guests(self, query):
        query = query.lower()
        guests = self.manager.list_guests()
        filtered_guests = [guest for guest in guests if query in guest[1].lower()]
        self.update_guest_table(filtered_guests)

    def delete_selected_guest(self):
        selected_row = self.guest_table.currentRow()
        if selected_row == -1:
            self.show_error("Please select a guest to delete.")
            return

        guest_id = int(self.guest_table.item(selected_row, 0).text())
        try:
            self.manager.delete_guest(guest_id)
            self.display_guests()
            self.show_info("Guest deleted successfully.")
        except Exception as e:
            self.show_error(f"Error deleting guest: {e}")

    # Make Reservation Tab
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
            self.show_error("All fields are required to make a reservation.")
            return
        if not self.is_valid_date(check_in) or not self.is_valid_date(check_out):
            self.show_error("Dates must be in the format YYYY-MM-DD.")
            return

        try:
            self.manager.make_reservation(guest_id, room_id, check_in, check_out)
            self.show_info(f"Reservation made for Guest ID {guest_id} in Room ID {room_id}.")
        except Exception as e:
            self.show_error(f"Error making reservation: {e}")

    # Reservation Overview Tab
    def reservation_overview_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.reservation_table = QTableWidget()
        self.reservation_table.setColumnCount(5)
        self.reservation_table.setHorizontalHeaderLabels(["ID", "Guest Name", "Room Number", "Check-In", "Check-Out"])
        self.reservation_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.reservation_table)

        refresh_button = QPushButton("Refresh Reservations")
        refresh_button.clicked.connect(self.display_reservations)
        layout.addWidget(refresh_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reservations")

    def display_reservations(self):
        reservations = self.manager.list_reservations()
        self.reservation_table.setRowCount(len(reservations))
        for row_index, reservation in enumerate(reservations):
            for col_index, data in enumerate(reservation):
                self.reservation_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    # Check Available Rooms Tab
    def check_available_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.room_search_input = QLineEdit()
        self.room_search_input.setPlaceholderText("Search Rooms...")
        self.room_search_input.textChanged.connect(self.search_rooms)
        layout.addWidget(self.room_search_input)

        self.room_table = QTableWidget()
        self.room_table.setColumnCount(3)
        self.room_table.setHorizontalHeaderLabels(["Room ID", "Room Number", "Type"])
        self.room_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.room_table)

        refresh_button = QPushButton("Refresh Rooms")
        refresh_button.clicked.connect(self.display_available_rooms)
        layout.addWidget(refresh_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Available Rooms")

    def display_available_rooms(self):
        rooms = self.manager.get_available_rooms()
        self.update_room_table(rooms)

    def update_room_table(self, rooms):
        self.room_table.setRowCount(len(rooms))
        for row_index, room in enumerate(rooms):
            for col_index, data in enumerate(room):
                self.room_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def search_rooms(self, query):
        query = query.lower()
        rooms = self.manager.get_available_rooms()
        filtered_rooms = [room for room in rooms if query in room[1].lower() or query in room[2].lower()]
        self.update_room_table(filtered_rooms)

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
