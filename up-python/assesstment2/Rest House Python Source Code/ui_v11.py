from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
    QStatusBar, QHeaderView, QDialog, QInputDialog
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from rest_house_manager_v5 import RestHouseManager
import re

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        layout.addWidget(self.password_input)

        login_button = QPushButton("Login")
        login_button.clicked.connect(self.authenticate)
        layout.addWidget(login_button)

        self.setLayout(layout)

        # Optional: Add a subtle shadow effect to the dialog
        # from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(15)
        # shadow.setOffset(0, 0)
        # self.setGraphicsEffect(shadow)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password":  # Replace with actual validation
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Invalid credentials")


class RestHouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = None
        try:
            self.manager = RestHouseManager()
            self.database_status = True
        except Exception as e:
            self.database_status = False
            self.show_error(f"Database Connection Error: {e}")

        self.setWindowTitle("Rest House Management System")
        self.setGeometry(100, 100, 800, 600)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()

        self.apply_theme()
        self.setup_pagination()

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_tabs()

        # Optional: Add a shadow to the main window central widget
        # from PyQt6.QtWidgets import QGraphicsDropShadowEffect
        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(20)
        # shadow.setOffset(0, 0)
        # self.centralWidget().setGraphicsEffect(shadow)

    def apply_theme(self):
        font = QFont("Open Sans", 10)
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
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                font-weight: bold;
            }

            /* Buttons */
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
                transition: background-color 0.3s ease;
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
                transition: border-color 0.3s ease;
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }

            /* Table */
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                gridline-color: #ddd;
                selection-background-color: #007bff;
                selection-color: #ffffff;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: 600;
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
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0;
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
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0;
            }

            /* StatusBar */
            QStatusBar {
                background-color: #e9ecef;
                padding: 4px;
            }

            /* Dialogs */
            QDialog {
                background-color: #f8f9fa;
            }
        """)

    def setup_pagination(self):
        self.page_size = 10
        self.current_page = 0
        self.total_pages = 0

    def update_status_bar(self):
        if self.database_status:
            self.status_bar.showMessage("Database Connected", 5000)
        else:
            self.status_bar.showMessage("Database Disconnected", 5000)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Info", message)

    def is_valid_contact(self, contact):
        phone_pattern = r"^\d{10,15}$"
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(phone_pattern, contact) or re.match(email_pattern, contact)

    def is_valid_name(self, name):
        return name.isalpha() and 2 <= len(name) <= 50

    def is_valid_date(self, date_str):
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        return re.match(pattern, date_str) is not None

    def init_tabs(self):
        self.add_guest_tab()
        self.list_guests_tab()
        self.make_reservation_tab()
        self.reservation_overview_tab()
        self.manage_rooms_tab()

    def paginate_table(self, data, table_widget):
        start = self.current_page * self.page_size
        end = start + self.page_size
        paginated_data = data[start:end]

        table_widget.setRowCount(len(paginated_data))
        for row_index, row_data in enumerate(paginated_data):
            for col_index, col_data in enumerate(row_data):
                table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def next_page(self, data, table_widget):
        if (self.current_page + 1) * self.page_size < len(data):
            self.current_page += 1
            self.paginate_table(data, table_widget)

    def previous_page(self, data, table_widget):
        if self.current_page > 0:
            self.current_page -= 1
            self.paginate_table(data, table_widget)

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
        # Provide a valid icon path or remove setIcon()
        # add_guest_button.setIcon(QIcon(":/icons/add_user.png"))  
        add_guest_button.clicked.connect(self.add_guest)
        layout.addWidget(add_guest_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Add Guest")

    def add_guest(self):
        name = self.guest_name_input.text().strip()
        contact = self.contact_input.text().strip()

        if not self.is_valid_name(name):
            self.show_error("Name must be alphabetic and between 2-50 characters.")
            return
        if not self.is_valid_contact(contact):
            self.show_error("Enter a valid phone number or email address.")
            return

        try:
            self.manager.add_guest(name, contact)
            self.guest_name_input.clear()
            self.contact_input.clear()
            self.show_info(f"Guest {name} added successfully.")
            self.manager.log_action("Add Guest", f"Guest {name} added.")
        except Exception as e:
            self.show_error(f"Error adding guest: {e}")

    def closeEvent(self, event):
        try:
            self.manager.close()
        except Exception as e:
            self.show_error(f"Error closing the database connection: {e}")
        event.accept()

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
        # refresh_button.setIcon(QIcon(":/icons/refresh.png"))
        refresh_button.clicked.connect(self.display_guests)
        layout.addWidget(refresh_button)

        delete_button = QPushButton("Delete Selected Guest")
        # delete_button.setIcon(QIcon(":/icons/delete_user.png"))
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
            self.manager.log_action("Delete Guest", f"Guest ID {guest_id} deleted.")
        except Exception as e:
            self.show_error(f"Error deleting guest: {e}")

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
        # make_reservation_button.setIcon(QIcon(":/icons/add_reservation.png"))
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
            self.manager.log_action("Make Reservation", f"Guest ID {guest_id} reserved Room ID {room_id}.")
        except Exception as e:
            self.show_error(f"Error making reservation: {e}")

    def reservation_overview_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.reservation_table = QTableWidget()
        self.reservation_table.setColumnCount(5)
        self.reservation_table.setHorizontalHeaderLabels(["ID", "Guest Name", "Room Number", "Check-In", "Check-Out"])
        self.reservation_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.reservation_table)

        refresh_button = QPushButton("Refresh Reservations")
        # refresh_button.setIcon(QIcon(":/icons/refresh.png"))
        refresh_button.clicked.connect(self.display_reservations)
        layout.addWidget(refresh_button)

        delete_button = QPushButton("Delete Selected Reservation")
        # delete_button.setIcon(QIcon(":/icons/delete_reservation.png"))
        delete_button.clicked.connect(self.delete_selected_reservation)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Reservations Overview")

    def display_reservations(self):
        try:
            reservations = self.manager.list_reservations()
            self.update_reservation_table(reservations)
        except Exception as e:
            self.show_error(f"Error fetching reservations: {e}")

    def update_reservation_table(self, reservations):
        self.reservation_table.setRowCount(len(reservations))
        for row_index, reservation in enumerate(reservations):
            for col_index, data in enumerate(reservation):
                self.reservation_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def delete_selected_reservation(self):
        selected_row = self.reservation_table.currentRow()
        if selected_row == -1:
            self.show_error("Please select a reservation to delete.")
            return

        reservation_id = int(self.reservation_table.item(selected_row, 0).text())
        try:
            self.manager.delete_reservation(reservation_id)
            self.display_reservations()
            self.show_info(f"Reservation ID {reservation_id} deleted successfully.")
            self.manager.log_action("Delete Reservation", f"Reservation ID {reservation_id} deleted.")
        except Exception as e:
            self.show_error(f"Error deleting reservation: {e}")

    def manage_rooms_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.room_table = QTableWidget()
        self.room_table.setColumnCount(4)
        self.room_table.setHorizontalHeaderLabels(["Room ID", "Room Number", "Type", "Status"])
        self.room_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.room_table)

        refresh_button = QPushButton("Refresh Rooms")
        # refresh_button.setIcon(QIcon(":/icons/refresh.png"))
        refresh_button.clicked.connect(self.display_rooms)
        layout.addWidget(refresh_button)

        add_button = QPushButton("Add Room")
        # add_button.setIcon(QIcon(":/icons/add_room.png"))
        add_button.clicked.connect(self.add_room)
        layout.addWidget(add_button)

        update_button = QPushButton("Update Selected Room")
        # update_button.setIcon(QIcon(":/icons/update_room.png"))
        update_button.clicked.connect(self.update_selected_room)
        layout.addWidget(update_button)

        delete_button = QPushButton("Delete Selected Room")
        # delete_button.setIcon(QIcon(":/icons/delete_room.png"))
        delete_button.clicked.connect(self.delete_selected_room)
        layout.addWidget(delete_button)

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Manage Rooms")

    def display_rooms(self):
        try:
            rooms = self.manager.get_available_rooms()
            self.update_room_table(rooms)
        except Exception as e:
            self.show_error(f"Error fetching rooms: {e}")

    def update_room_table(self, rooms):
        self.room_table.setRowCount(len(rooms))
        for row_index, room in enumerate(rooms):
            for col_index, data in enumerate(room):
                self.room_table.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def add_room(self):
        room_number, room_type = self.get_room_input()
        if not room_number or not room_type:
            self.show_error("Room Number and Type are required.")
            return

        try:
            self.manager.add_room(room_number, room_type)
            self.show_info(f"Room {room_number} added successfully.")
            self.display_rooms()
            self.manager.log_action("Add Room", f"Room {room_number} added.")
        except Exception as e:
            self.show_error(f"Error adding room: {e}")

    def update_selected_room(self):
        selected_row = self.room_table.currentRow()
        if selected_row == -1:
            self.show_error("Please select a room to update.")
            return

        room_id = int(self.room_table.item(selected_row, 0).text())
        new_room_type = self.get_input("Update Room Type", "Enter new room type:")
        if not new_room_type:
            self.show_error("Room type cannot be empty.")
            return

        try:
            self.manager.update_room(room_id, new_room_type)
            self.show_info(f"Room ID {room_id} updated to type {new_room_type}.")
            self.display_rooms()
            self.manager.log_action("Update Room", f"Room ID {room_id} updated to type {new_room_type}.")
        except Exception as e:
            self.show_error(f"Error updating room: {e}")

    def delete_selected_room(self):
        selected_row = self.room_table.currentRow()
        if selected_row == -1:
            self.show_error("Please select a room to delete.")
            return

        room_id = int(self.room_table.item(selected_row, 0).text())
        try:
            self.manager.delete_room(room_id)
            self.show_info(f"Room ID {room_id} deleted successfully.")
            self.display_rooms()
            self.manager.log_action("Delete Room", f"Room ID {room_id} deleted.")
        except Exception as e:
            self.show_error(f"Error deleting room: {e}")

    def get_room_input(self):
        room_number = self.get_input("Add Room", "Enter Room Number:")
        room_type = self.get_input("Add Room", "Enter Room Type (e.g., Single, Double, Suite):")
        return room_number, room_type

    def get_input(self, title, message):
        text, ok = QInputDialog.getText(self, title, message)
        return text if ok else None


if __name__ == "__main__":
    app = QApplication([])
    login = LoginDialog()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = RestHouseApp()
        window.show()
        app.exec()
