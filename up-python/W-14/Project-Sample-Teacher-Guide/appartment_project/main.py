# appartment_project/main.py
import sqlite3
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QMainWindow, QMdiArea, QMdiSubWindow
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from all_forms.dashboard_form import Dashboard
from all_forms.bills_form import BillsScreen
from all_forms.users_form import UsersScreen
from all_forms.payments_form import PaymentsScreen
from all_forms.apartment_form import ApartmentScreen
import pretty_errors

pretty_errors.configure(
    separator_character='#',
    filename_display=pretty_errors.FILENAME_FULL,
    lines_before=5,
    lines_after=5,
)


class Menu(QWidget):
    def __init__(self, mdi_area):
        super().__init__()
        self.mdi_area = mdi_area

        self.setFont(QFont("Khmer OS", 12))  # Set Khmer font with size 12

        # Buttons for menu
        self.dashboard_button = QPushButton("Dashboard")
        self.apartment_button = QPushButton("Apartment")
        self.users_button = QPushButton("Users")
        self.payments_button = QPushButton("Payments")
        self.bills_button = QPushButton("Bills")

        # Layout for menu
        layout = QVBoxLayout()
        layout.addWidget(self.dashboard_button)
        layout.addWidget(self.apartment_button)
        layout.addWidget(self.users_button)
        layout.addWidget(self.payments_button)
        layout.addWidget(self.bills_button)

        # Button click connections
        self.dashboard_button.clicked.connect(self.open_dashboard)
        self.apartment_button.clicked.connect(self.open_apartments_screen)
        self.users_button.clicked.connect(self.open_users_screen)
        self.payments_button.clicked.connect(self.open_payments_screen)
        self.bills_button.clicked.connect(self.open_bills_screen)

        self.setLayout(layout)

    def open_dashboard(self):
        self._open_window("Dashboard", Dashboard())

    def open_apartments_screen(self):
        self._open_window("Apartments", ApartmentScreen())

    def open_users_screen(self):
        self._open_window("Users", UsersScreen())

    def open_payments_screen(self):
        self._open_window("Payments", PaymentsScreen())

    def open_bills_screen(self):
        self._open_window("Bills", BillsScreen())

    def _open_window(self, title, widget):
        for subwindow in self.mdi_area.subWindowList():
            if subwindow.windowTitle() == title:
                self.mdi_area.setActiveSubWindow(subwindow)
                subwindow.showMaximized()  # Maximize the existing subwindow
                return
        subwindow = QMdiSubWindow()
        subwindow.setWidget(widget)
        subwindow.setWindowTitle(title)
        self.mdi_area.addSubWindow(subwindow)
        subwindow.showMaximized()  # Maximize the newly created subwindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("APARTMENT MANAGEMENT SYSTEM")
        self.setFont(QFont("Khmer OS", 12))  # Set Khmer font with size 12

        # Create main layout
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # MDI area
        self.mdi_area = QMdiArea()

        # Menu
        self.menu = Menu(self.mdi_area)
        self.menu.setFixedWidth(200)

        # Add menu and MDI area to layout
        main_layout.addWidget(self.menu)
        main_layout.addWidget(self.mdi_area)

        # Set main widget and layout
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Khmer OS", 12))  # Set application-wide Khmer font

    window = MainApp()
    window.resize(900, 600)
    window.show()

    sys.exit(app.exec())
