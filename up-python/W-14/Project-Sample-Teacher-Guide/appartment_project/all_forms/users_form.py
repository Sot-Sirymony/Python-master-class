import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtGui import QFont
from Database.dao import AccessDatabase
from Database.dto import ModifyDatabase
from Classes.dbClasses import User, Bill
import matplotlib.pyplot as plt


class UsersScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Input fields and labels
        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        self.debts_label = QLabel("Debts")
        self.debts_input = QLineEdit()
        self.apt_label = QLabel("Apartment No")
        self.apt_input = QLineEdit()

        # Buttons
        self.add_button = QPushButton("Add User")
        self.delete_button = QPushButton("Delete User")
        self.graph_button1 = QPushButton("Plot User Bills")
        self.graph_button2 = QPushButton("Plot User Payments")

        # Add widgets to layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.apt_label)
        layout.addWidget(self.apt_input)
        layout.addWidget(self.debts_label)
        layout.addWidget(self.debts_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.graph_button1)
        layout.addWidget(self.graph_button2)

        # Connect buttons to methods
        self.add_button.clicked.connect(self.add_user)
        self.delete_button.clicked.connect(self.delete_user)
        self.graph_button1.clicked.connect(self.plot_graphs1)
        self.graph_button2.clicked.connect(self.plot_graphs2)

        # User table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Debts", "Apartment No"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setColumnWidth(0, 80)
        self.table.setColumnWidth(1, 140)
        self.table.setColumnWidth(2, 180)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        layout.addWidget(self.table)

        # Populate the table with data
        self.view_table()

        self.setLayout(layout)

    def view_table(self):
        """Fetch and display all users."""
        try:
            users = AccessDatabase().getAllUsers()
            self.table.setRowCount(len(users))
            for i, user in enumerate(users):
                self.table.setItem(i, 0, QTableWidgetItem(str(user[0])))  # User ID
                self.table.setItem(i, 1, QTableWidgetItem(user[1]))       # Name
                self.table.setItem(i, 2, QTableWidgetItem(user[2]))       # Email
                self.table.setItem(i, 3, QTableWidgetItem(str(user[3])))  # Debts
                self.table.setItem(i, 4, QTableWidgetItem(str(user[4])))  # Apartment No
        except Exception as e:
            self.show_message(f"Failed to load users: {e}", error=True)

    def add_user(self):
        """Add a new user."""
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()
        aptNo = self.apt_input.text().strip()
        debts = self.debts_input.text().strip()

        # Input validation
        if not name or not email or not aptNo:
            self.show_message("Name, Email, and Apartment No are required fields.", error=True)
            return
        if debts and not debts.isdigit():
            self.show_message("Debts must be a numeric value.", error=True)
            return
        if not aptNo.isdigit():
            self.show_message("Apartment No must be a numeric value.", error=True)
            return

        try:
            debts = int(debts) if debts else 0  # Default debts to 0 if not provided
            user = User(user_id=None, name=name, email=email, aptNo=int(aptNo), debts=debts)
            ModifyDatabase().addUser(user)
            self.view_table()
            self.show_message("User added successfully!")
        except Exception as e:
            self.show_message(f"Failed to add user: {e}", error=True)

    def delete_user(self):
        """Delete the selected user."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select a user to delete.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            user_id = int(id_item.text())
            ModifyDatabase().deleteUser(user_id)
            self.view_table()
            self.show_message("User deleted successfully!")
        except Exception as e:
            self.show_message(f"Failed to delete user: {e}", error=True)

    def plot_graphs1(self):
        """Plot user bills graph."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select a user to plot bills.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            user_id = int(id_item.text())
            user_bills = AccessDatabase().getAllUserBills(user_id=user_id)

            amounts = [bill[1] for bill in user_bills]
            due_dates = [bill[2] for bill in user_bills]

            plt.plot(due_dates, amounts, marker='o')
            plt.xlabel("Due Dates")
            plt.ylabel("Amounts")
            plt.title("User Bills")
            plt.grid(True)
            plt.show()
        except Exception as e:
            self.show_message(f"Failed to plot user bills: {e}", error=True)

    def plot_graphs2(self):
        """Plot user payments graph."""
        selected_row = self.table.currentRow()

        if selected_row < 0:
            self.show_message("Please select a user to plot payments.", error=True)
            return

        try:
            id_item = self.table.item(selected_row, 0)
            user_id = int(id_item.text())
            user_bills = AccessDatabase().getAllUserBills(user_id=user_id)

            amounts = []
            dates = []
            for bill in user_bills:
                bill_id = bill[0]
                user_payments = AccessDatabase().getAllUserPayments(bill_id=bill_id)
                amounts.extend([payment[1] for payment in user_payments])
                dates.extend([payment[2] for payment in user_payments])

            plt.plot(dates, amounts, marker='o')
            plt.xlabel("Dates")
            plt.ylabel("Amounts")
            plt.title("User Payments")
            plt.grid(True)
            plt.show()
        except Exception as e:
            self.show_message(f"Failed to plot user payments: {e}", error=True)

    def show_message(self, message, error=False):
        """Display a message box."""
        msg = QMessageBox()
        msg.setText(message)
        msg.setFont(QFont("Khmer OS", 12))  # Khmer font for localization
        msg.setIcon(QMessageBox.Icon.Critical if error else QMessageBox.Icon.Information)
        msg.setWindowTitle("Error" if error else "Message")
        msg.exec()
