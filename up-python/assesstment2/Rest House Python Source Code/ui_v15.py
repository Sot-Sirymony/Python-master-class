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
        self.setGeometry(100, 100, 800, 600)

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
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: #ffffff;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                border-radius: 4px;
                padding: 8px 16px;
                color: #333;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                font-weight: bold;
                color: #007bff;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                color: #000;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
            }
            QStatusBar {
                background-color: #e9ecef;
                padding: 4px;
            }
        """)

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

        guests_card = self.create_dashboard_card("Total Guests", total_guests)
        rooms_card = self.create_dashboard_card("Total Rooms", total_rooms)
        available_card = self.create_dashboard_card("Available Rooms", available_rooms)
        occupied_card = self.create_dashboard_card("Occupied Rooms", occupied_rooms)
        reservation_progress = self.create_reservation_progress(total_reservations, total_rooms)

        layout.addWidget(guests_card, 0, 0)
        layout.addWidget(rooms_card, 0, 1)
        layout.addWidget(available_card, 1, 0)
        layout.addWidget(occupied_card, 1, 1)
        layout.addWidget(reservation_progress, 2, 0, 1, 2)

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

    def create_reservation_progress(self, reservations, total_rooms):
        group = QGroupBox("Reservations Progress")
        layout = QVBoxLayout()
        progress = QProgressBar()
        progress.setMaximum(total_rooms)
        progress.setValue(reservations)
        progress.setFormat(f"{reservations} / {total_rooms} Reservations")
        layout.addWidget(progress)
        group.setLayout(layout)
        return group

    # Guest Management Tab
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
        delete_button.clicked.connect(self.delete_selected_guest)

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

    def delete_selected_guest(self):
        selected_row = self.guest_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Please select a guest to delete.")
            return
        guest_id = int(self.guest_table.item(selected_row, 0).text())
        try:
            self.manager.delete_guest(guest_id)
            QMessageBox.information(self, "Success", "Guest deleted successfully.")
            self.display_guests()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # Room Management Tab
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
        update_button.clicked.connect(self.update_selected_room)
        delete_button.clicked.connect(self.delete_selected_room)
        refresh_button.clicked.connect(self.display_rooms)

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(delete_button)
        button_layout.addWidget(refresh_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
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
        room_number = self.room_number_input.text().strip()
        room_type = self.room_type_input.text().strip()
        if not room_number or not room_type:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return
        try:
            self.manager.add_room(room_number, room_type)
            QMessageBox.information(self, "Success", "Room added successfully.")
            self.display_rooms()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def update_selected_room(self):
        selected_row = self.room_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Select a room to update.")
            return
        room_id = int(self.room_table.item(selected_row, 0).text())
        room_type = self.room_type_input.text().strip()
        status = self.room_status_combo.currentText()
        try:
            self.manager.update_room(room_id, room_type, status)
            QMessageBox.information(self, "Success", "Room updated successfully.")
            self.display_rooms()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def delete_selected_room(self):
        selected_row = self.room_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Select a room to delete.")
            return
        room_id = int(self.room_table.item(selected_row, 0).text())
        self.manager.delete_room(room_id)
        QMessageBox.information(self, "Success", "Room deleted successfully.")
        self.display_rooms()

    def closeEvent(self, event):
        self.manager.close()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RestHouseApp()
    window.show()
    sys.exit(app.exec())
