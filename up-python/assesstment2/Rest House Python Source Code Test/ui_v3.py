from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar, QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from rest_house_manager import RestHouseManager
import csv


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
        self.add_room_tab()
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
            self.show_error("Both Room Number and Room Type are required.")
            return

        try:
            self.manager.add_room(room_number, room_type)
            self.room_number_input.clear()
            self.room_type_input.clear()
            self.show_info(f"Room {room_number} added successfully.")
        except Exception as e:
            self.show_error(f"Error adding room: {e}")

    def check_available_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Table for available rooms
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(3)
        self.room_table.setHorizontalHeaderLabels(["Room ID", "Room Number", "Type"])
        self.room_table.setSortingEnabled(True)
        self.room_table.horizontalHeader().setStretchLastSection(True)
        self.room_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.room_table)

        # Button to refresh and display available rooms
        refresh_button = QPushButton("Refresh Rooms")
        refresh_button.clicked.connect(self.display_available_rooms)
        layout.addWidget(refresh_button)

        # Button to export to CSV
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(export_button)

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

    def export_to_csv(self):
        try:
            rooms = self.manager.get_available_rooms()
            if not rooms:
                self.show_error("No available rooms to export.")
                return

            file_path = "available_rooms.csv"
            with open(file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Room ID", "Room Number", "Type"])
                writer.writerows(rooms)

            self.show_info(f"Available rooms exported to {file_path}.")
        except Exception as e:
            self.show_error(f"Error exporting rooms to CSV: {e}")

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
