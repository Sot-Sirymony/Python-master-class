import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QDateEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import Bill
from Email.reminder_emails import send_reminder_email
import os

def parse_date(date_str):
        """Parse a date string into a standardized format."""
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m-%d-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Date format not recognized: {date_str}")
    
class BillsScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Input Fields and Buttons
        self.label1 = QLabel("Amount")
        self.amount_input = QLineEdit()
        self.label2 = QLabel("Due Date")
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)  # Enable calendar popup for date input
        self.label3 = QLabel("User ID")
        self.user_id_input = QLineEdit()
        self.label4 = QLabel("Details")
        self.details_input = QLineEdit()
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")

        layout.addWidget(self.label1)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.label2)
        layout.addWidget(self.due_date_input)
        layout.addWidget(self.label3)
        layout.addWidget(self.user_id_input)
        layout.addWidget(self.label4)
        layout.addWidget(self.details_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)

        self.add_button.clicked.connect(self.add_bill)
        self.delete_button.clicked.connect(self.delete_bill)

        # Table for displaying bills
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Bill ID", "Amount", "Due Date", "Details", "User ID"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(4, 80)
        self.view_table()

        layout.addWidget(self.table)
        self.setLayout(layout)

        # Check and send bill reminder emails
        self.bills_reminder_email()

    def view_table(self):
        """Fetch and display all bills."""
        try:
            bills = AccessDatabase().getAllBills()
            self.table.setRowCount(len(bills))
            for i, bill in enumerate(bills):
                self.table.setItem(i, 0, QTableWidgetItem(str(bill[0])))  # Bill ID
                self.table.setItem(i, 1, QTableWidgetItem(str(bill[1])))  # Amount
                self.table.setItem(i, 2, QTableWidgetItem(str(bill[2])))  # Due Date
                self.table.setItem(i, 3, QTableWidgetItem(str(bill[3])))  # Details
                self.table.setItem(i, 4, QTableWidgetItem(str(bill[4])))  # User ID
        except Exception as e:
            self.show_message(f"Error loading bills: {e}", error=True)

    def add_bill(self):
        """Add a new bill."""
        amount = self.amount_input.text().strip()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")
        details = self.details_input.text().strip()
        user_id = self.user_id_input.text().strip()

        # Input Validation
        if not amount or not user_id or not details:
            self.show_message("Amount, User ID, and Details are required fields.", error=True)
            return
        if not amount.isdigit() or not user_id.isdigit():
            self.show_message("Amount and User ID must be numeric.", error=True)
            return

        try:
            bill = Bill(bill_id=None, amount=int(amount), due_date=due_date, user_id=int(user_id), details=details)
            ModifyDatabase().addBill(bill)
            self.view_table()
            self.show_message("Bill added successfully!")
        except Exception as e:
            self.show_message(f"Failed to add bill: {e}", error=True)

    def delete_bill(self):
        """Delete the selected bill."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select a bill to delete.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            bill_id = int(id_item.text())

            ModifyDatabase().deleteBill(bill_id)
            self.view_table()
            self.show_message("Bill deleted successfully!")
        except Exception as e:
            self.show_message(f"Failed to delete bill: {e}", error=True)

    def bills_reminder_email(self):
        """Send reminder emails for overdue bills."""
        try:
            bills = AccessDatabase().getAllBills()
            for bill in bills:
                bill_id = str(bill[0])
                amount = str(bill[1])
                due_date = str(bill[2])
                details = str(bill[3])
                user_id = str(bill[4])

                # Parse the due date using the new parse_date function
                try:
                    date_object = parse_date(due_date)
                except ValueError as e:
                    self.show_message(f"Error parsing due date: {e}", error=True)
                    continue

                # Check if the due date has passed
                if date_object < datetime.now().date():
                    user = AccessDatabase().getUser(int(user_id))
                    recipient_email = user.email

                    subject = "Bill Reminder"
                    message = (
                        f"Dear {user.name},\n\n"
                        f"Your bill (ID: {bill_id}) of amount {amount} is overdue. Details: {details}.\n"
                        f"Please make the payment at your earliest convenience.\n\n"
                        "Thank you."
                    )
                    try:
                        send_reminder_email(recipient_email=recipient_email, subject=subject, message=message)
                        self.show_message(f"Reminder email sent to {recipient_email}")
                    except Exception as e:
                        self.show_message(f"Failed to send email: {e}", error=True)

        except Exception as e:
            self.show_message(f"Failed to send reminder emails: {e}", error=True)

    def send_reminder_email(recipient_email, subject, message):
        try:
            # Check if account.txt exists
            if not os.path.exists("account.txt"):
                raise FileNotFoundError("The account.txt file is missing. Please add it to the project directory.")
            
            # Read email credentials from account.txt
            with open("account.txt", "r") as file:
                lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("The account.txt file must contain at least two lines: email and password.")
                sender_email = lines[0].strip()
                sender_password = lines[1].strip()

            # Simulate email sending (replace this with actual email-sending logic)
            print(f"Sending email to {recipient_email} from {sender_email}...")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            # Actual email-sending logic would go here

        except FileNotFoundError as e:
            raise FileNotFoundError(f"Failed to send email: {e}")
        except Exception as e:
            raise Exception(f"An error occurred while sending the email: {e}")
    
    def show_message(self, message, error=False):
        """Display a message box."""
        msg = QMessageBox()
        msg.setText(message)
        msg.setFont(QFont("Khmer OS", 12))  # Khmer font for messages
        msg.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
        msg.setWindowTitle("Error" if error else "Message")
        msg.exec()
