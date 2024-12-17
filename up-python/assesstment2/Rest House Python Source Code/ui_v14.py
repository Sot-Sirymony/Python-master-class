from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QProgressBar, QTableWidget, QTableWidgetItem, QMessageBox, QStatusBar,
    QGroupBox, QGridLayout, QLineEdit, QPushButton, QFormLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from rest_house_manager_v7 import RestHouseManager

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
            /* Tabs */
            QTabWidget::pane {
                border: 1px solid #ccc;
                background: #ffffff;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                border-radius: 4px;
                padding: 8px 16px;
                margin: 2px;
                font-weight: 500;
                color: #333;  /* Dark text */
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                font-weight: bold;
                color: #007bff; /* Blue for selected tabs */
            }
            /* Buttons */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #ccc;
                color: #666;
            }
            /* LineEdit */
            QLineEdit {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 4px;
                background-color: #ffffff;
                color: #000000;  /* Black text */
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }
            /* Table */
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                gridline-color: #ddd;
                color: #000000;  /* Black text */
                selection-background-color: #007bff;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: 600;
                color: #333;  /* Dark text */
            }
            /* Scrollbars */
            QScrollBar:vertical {
                background: #f1f1f1;
                width: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #007bff;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #0056b3;
            }
            QScrollBar:horizontal {
                background: #f1f1f1;
                height: 12px;
                margin: 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #007bff;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #0056b3;
            }
            /* StatusBar */
            QStatusBar {
                background-color: #e9ecef;
                padding: 4px;
                color: #333;  /* Dark text */
            }
            /* Dialogs */
            QDialog {
                background-color: #f8f9fa;
                color: #333;  /* Dark text */
            }
            /* GroupBox */
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                margin-top: 20px;
                background-color: #ffffff;
                color: #333;  /* Dark text */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                font-weight: bold;
                color: #007bff;  /* Blue title */
            }
        """)
    def init_tabs(self):
        self.dashboard_tab()
        self.list_guests_tab()
        self.manage_rooms_tab()

    def dashboard_tab(self):
        tab = QWidget()
        layout = QGridLayout()

        # Retrieve Metrics
        total_guests = len(self.manager.list_guests())
        total_rooms = len(self.manager.get_available_rooms()) + len(self.manager.get_occupied_rooms())
        available_rooms = len(self.manager.get_available_rooms())
        occupied_rooms = total_rooms - available_rooms
        total_reservations = len(self.manager.list_reservations())

        # Create Cards
        guests_card = self.create_dashboard_card("Total Guests", str(total_guests))
        rooms_card = self.create_dashboard_card("Total Rooms", str(total_rooms))
        available_card = self.create_dashboard_card("Available Rooms", str(available_rooms))
        occupied_card = self.create_dashboard_card("Occupied Rooms", str(occupied_rooms))
        reservation_progress = self.create_reservation_progress("Reservations", total_reservations, total_rooms)

        # Add to Layout
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
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        group.setLayout(layout)
        return group

    def create_reservation_progress(self, title, reservations, total_rooms):
        group = QGroupBox(title)
        layout = QVBoxLayout()
        progress_bar = QProgressBar()
        progress_bar.setMaximum(total_rooms)
        progress_bar.setValue(reservations)
        progress_bar.setFormat(f"{reservations} / {total_rooms} Reservations")
        layout.addWidget(progress_bar)
        group.setLayout(layout)
        return group

    def list_guests_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.guest_table = QTableWidget()
        self.guest_table.setColumnCount(3)
        self.guest_table.setHorizontalHeaderLabels(["ID", "Name", "Contact"])
        layout.addWidget(self.guest_table)

        refresh_button = QPushButton("Refresh Guests")
        refresh_button.clicked.connect(self.display_guests)
        layout.addWidget(refresh_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "List Guests")

    def display_guests(self):
        guests = self.manager.list_guests()
        self.guest_table.setRowCount(len(guests))
        for row, guest in enumerate(guests):
            for col, value in enumerate(guest):
                self.guest_table.setItem(row, col, QTableWidgetItem(str(value)))

    def manage_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(4)
        self.room_table.setHorizontalHeaderLabels(["ID", "Room Number", "Type", "Status"])
        layout.addWidget(self.room_table)

        refresh_button = QPushButton("Refresh Rooms")
        refresh_button.clicked.connect(self.display_rooms)
        layout.addWidget(refresh_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Rooms")

    def display_rooms(self):
        rooms = self.manager.get_available_rooms() + self.manager.get_occupied_rooms()
        self.room_table.setRowCount(len(rooms))
        for row, room in enumerate(rooms):
            for col, value in enumerate(room):
                self.room_table.setItem(row, col, QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.manager.close()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = RestHouseApp()
    window.show()
    sys.exit(app.exec())
