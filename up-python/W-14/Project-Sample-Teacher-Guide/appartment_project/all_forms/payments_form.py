import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Payment


class PaymentsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Input Fields and Buttons
        self.label1 = QLabel("Amount")
        self.amount_input = QLineEdit()
        self.label2 = QLabel("Date")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Show calendar popup for date selection
        self.label3 = QLabel("Bill ID")
        self.bill_id_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.label1)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.date_input)
        layout.addWidget(self.label3)
        layout.addWidget(self.bill_id_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        self.add_button.clicked.connect(self.add_payment)
        self.delete_button.clicked.connect(self.delete_payment)

        # Payment Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Amount", "Date", "Bill ID"])
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Populate Table
        self.view_table()

    def view_table(self):
        """Fetch and display all payments."""
        try:
            payments = AccessDatabase().getAllPayments()
            self.table.setRowCount(len(payments))
            for i, payment in enumerate(payments):
                self.table.setItem(i, 0, QTableWidgetItem(str(payment[0])))  # Payment ID
                self.table.setItem(i, 1, QTableWidgetItem(str(payment[1])))  # Amount
                self.table.setItem(i, 2, QTableWidgetItem(str(payment[2])))  # Date
                self.table.setItem(i, 3, QTableWidgetItem(str(payment[3])))  # Bill ID
        except Exception as e:
            self.show_message(f"Error loading payments: {e}", error=True)

    def add_payment(self):
        """Add a new payment."""
        amount = self.amount_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        bill_id = self.bill_id_input.text().strip()

        # Validate inputs
        if not amount or not bill_id:
            self.show_message("Amount and Bill ID are required.", error=True)
            return
        if not amount.isdigit() or not bill_id.isdigit():
            self.show_message("Amount and Bill ID must be numeric.", error=True)
            return

        try:
            payment = Payment(id=None, amount=int(amount), date=date, bill_id=int(bill_id))
            ModifyDatabase().addPayment(payment)
            self.view_table()
            self.show_message("Payment added successfully!")
        except Exception as e:
            self.show_message(f"Failed to add payment: {e}", error=True)

    def delete_payment(self):
        """Delete the selected payment."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select a payment to delete.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            payment_id = int(id_item.text())

            ModifyDatabase().deletePayment(payment_id)
            self.view_table()
            self.show_message("Payment deleted successfully!")
        except Exception as e:
            self.show_message(f"Failed to delete payment: {e}", error=True)

    def show_message(self, message, error=False):
        """Display a message box."""
        msg = QMessageBox()
        msg.setText(message)
        msg.setFont(QFont("Khmer OS", 12))  # Khmer font for messages
        msg.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
        msg.setWindowTitle("Error" if error else "Message")
        msg.exec()
