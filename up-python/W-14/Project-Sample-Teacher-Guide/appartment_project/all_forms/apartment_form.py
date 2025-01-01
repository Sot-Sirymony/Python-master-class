import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont
from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Apartment


class ApartmentScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Input Fields and Buttons
        self.aptNo_label = QLabel("Apartment No")
        self.aptNo_input = QLineEdit()
        self.status_label = QLabel("Status")
        self.status_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.aptNo_label)
        layout.addWidget(self.aptNo_input)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        self.add_button.clicked.connect(self.add_apt)
        self.delete_button.clicked.connect(self.delete_apt)

        # Apartment Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Apartment No", "Status"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(self.table)

        self.setLayout(layout)

        # Populate Table
        self.view_table()

    def view_table(self):
        """Fetch and display all apartments."""
        try:
            apartments = AccessDatabase().getAllApartments()
            self.table.setRowCount(len(apartments))
            for i, apt in enumerate(apartments):
                self.table.setItem(i, 0, QTableWidgetItem(str(apt[0])))
                self.table.setItem(i, 1, QTableWidgetItem(str(apt[1])))
        except Exception as e:
            self.show_message(f"Failed to load apartments: {e}", error=True)

    def add_apt(self):
        """Add a new apartment."""
        aptNo = self.aptNo_input.text().strip()
        status = self.status_input.text().strip()

        # Validate inputs
        if not aptNo or not status:
            self.show_message("Please fill in all fields.", error=True)
            return

        try:
            apt = Apartment(aptNo=int(aptNo), status=status)
            ModifyDatabase().addApartment(apt)
            self.view_table()
            self.show_message("Apartment added successfully!")
        except ValueError:
            self.show_message("Apartment No must be a number.", error=True)
        except Exception as e:
            self.show_message(f"Failed to add Apartment: {e}", error=True)

    def delete_apt(self):
        """Delete the selected apartment."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select an apartment to delete.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            row_id = int(id_item.text())
            ModifyDatabase().deleteApartment(row_id)
            self.table.removeRow(selected_row)
            self.show_message("Apartment deleted successfully!")
        except Exception as e:
            self.show_message(f"Failed to delete Apartment: {e}", error=True)

    def show_message(self, message, error=False):
        """Display a message box."""
        msg = QMessageBox()
        msg.setText(message)
        msg.setFont(QFont("Khmer OS", 12))  # Khmer font for messages
        msg.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
        msg.setWindowTitle("Error" if error else "Message")
        msg.exec()
