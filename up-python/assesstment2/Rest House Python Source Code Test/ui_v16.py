from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QProgressBar, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar,
    QGroupBox, QGridLayout, QLineEdit, QPushButton, QFormLayout, QComboBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from rest_house_manager_v8 import RestHouseManager


class RestHouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = RestHouseManager()

        self.setWindowTitle("Rest House Management System")
        self.setGeometry(100, 100, 900, 600)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Database Connected")

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.apply_theme()
        self.init_tabs()

    def apply_theme(self):
        font = QFont("Sans-Serif", 10)
        self.setFont(font)

    def init_tabs(self):
        self.dashboard_tab()
        self.list_guests_tab()
        self.manage_rooms_tab()
        self.manage_reservations_tab()

    # Dashboard Tab
    def dashboard_tab(self):
        tab = QWidget()
        layout = QGridLayout()

        total_guests = len(self.manager.get_all_guests())
        total_rooms = len(self.manager.get_all_rooms())
        available_rooms = len(self.manager.get_available_rooms())
        occupied_rooms = total_rooms - available_rooms
        total_reservations = len(self.manager.get_all_reservations())

        layout.addWidget(self.create_dashboard_card("Total Guests", total_guests), 0, 0)
        layout.addWidget(self.create_dashboard_card("Total Rooms", total_rooms), 0, 1)
        layout.addWidget(self.create_dashboard_card("Available Rooms", available_rooms), 1, 0)
        layout.addWidget(self.create_dashboard_card("Occupied Rooms", occupied_rooms), 1, 1)

        progress = QProgressBar()
        progress.setMaximum(total_rooms)
        progress.setValue(total_reservations)
        progress.setFormat(f"{total_reservations} / {total_rooms} Reservations")
        layout.addWidget(progress, 2, 0, 1, 2)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Dashboard")

    def create_dashboard_card(self, title, value):
        group = QGroupBox(title)
        layout = QVBoxLayout()
        label = QLabel(str(value))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)
        group.setLayout(layout)
        return group

    # Guest Management
    def list_guests_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.guest_table = QTableWidget()
        self.guest_table.setColumnCount(3)
        self.guest_table.setHorizontalHeaderLabels(["ID", "Name", "Contact"])
        layout.addWidget(self.guest_table)

        button_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh Guests")
        delete_button = QPushButton("Delete Guest")

        refresh_button.clicked.connect(self.display_guests)
        delete_button.clicked.connect(self.delete_guest)

        button_layout.addWidget(refresh_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Guests")
        self.display_guests()

    def display_guests(self):
        guests = self.manager.get_all_guests()
        self.guest_table.setRowCount(len(guests))
        for row, guest in enumerate(guests):
            for col, value in enumerate(guest):
                self.guest_table.setItem(row, col, QTableWidgetItem(str(value)))

    def delete_guest(self):
        row = self.guest_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a guest to delete.")
            return
        guest_id = int(self.guest_table.item(row, 0).text())
        try:
            self.manager.delete_guest(guest_id)
            QMessageBox.information(self, "Success", "Guest deleted successfully.")
            self.display_guests()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # Room Management
    def manage_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.room_table = QTableWidget()
        self.room_table.setColumnCount(4)
        self.room_table.setHorizontalHeaderLabels(["ID", "Room Number", "Type", "Status"])
        layout.addWidget(self.room_table)

        form_layout = QFormLayout()
        self.room_number_input = QLineEdit()
        self.room_type_input = QLineEdit()
        self.room_status_combo = QComboBox()
        self.room_status_combo.addItems(["available", "occupied", "maintenance"])

        form_layout.addRow("Room Number:", self.room_number_input)
        form_layout.addRow("Room Type:", self.room_type_input)
        form_layout.addRow("Status:", self.room_status_combo)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Room")
        update_button = QPushButton("Update Room")
        delete_button = QPushButton("Delete Room")
        refresh_button = QPushButton("Refresh Rooms")

        add_button.clicked.connect(self.add_room)
        update_button.clicked.connect(self.update_room)
        delete_button.clicked.connect(self.delete_room)
        refresh_button.clicked.connect(self.display_rooms)

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.room_table)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Rooms")
        self.display_rooms()

    def display_rooms(self):
        rooms = self.manager.get_all_rooms()
        self.room_table.setRowCount(len(rooms))
        for row, room in enumerate(rooms):
            for col, value in enumerate(room):
                self.room_table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_room(self):
        room_number = self.room_number_input.text()
        room_type = self.room_type_input.text()
        if not room_number or not room_type:
            QMessageBox.warning(self, "Input Error", "Room number and type are required.")
            return
        self.manager.add_room(room_number, room_type)
        QMessageBox.information(self, "Success", "Room added successfully.")
        self.display_rooms()

    def update_room(self):
        row = self.room_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection Error", "Select a room to update.")
            return
        room_id = int(self.room_table.item(row, 0).text())
        room_type = self.room_type_input.text()
        status = self.room_status_combo.currentText()
        self.manager.update_room(room_id, room_type, status)
        QMessageBox.information(self, "Success", "Room updated successfully.")
        self.display_rooms()

    def delete_room(self):
        row = self.room_table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Selection Error", "Select a room to delete.")
            return
        room_id = int(self.room_table.item(row, 0).text())
        self.manager.delete_room(room_id)
        QMessageBox.information(self, "Success", "Room deleted successfully.")
        self.display_rooms()

    # Reservations Tab
    def manage_reservations_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.reservation_table = QTableWidget()
        self.reservation_table.setColumnCount(6)
        self.reservation_table.setHorizontalHeaderLabels(["ID", "Guest", "Room", "Check-in", "Check-out", "Status"])
        layout.addWidget(self.reservation_table)

        button_layout = QHBoxLayout()
        refresh_button = QPushButton("Refresh Reservations")
        refresh_button.clicked.connect(self.display_reservations)
        button_layout.addWidget(refresh_button)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Reservations")
        self.display_reservations()

    def display_reservations(self):
        reservations = self.manager.get_all_reservations()
        self.reservation_table.setRowCount(len(reservations))
        for row, reservation in enumerate(reservations):
            for col, value in enumerate(reservation):
                self.reservation_table.setItem(row, col, QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.manager.close()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RestHouseApp()
    window.show()
    sys.exit(app.exec())
