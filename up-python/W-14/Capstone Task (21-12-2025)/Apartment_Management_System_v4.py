import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QLabel, QHBoxLayout, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt
from sql_lite_script_v2 import initialize_database

# Helper function for SQLite queries
def execute_query(query, params=()):
    try:
        conn = sqlite3.connect("apartment_management.db")
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
        QMessageBox.critical(None, "Database Error", f"An error occurred: {e}")
        return None


class ApartmentManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Apartment Management System")
        self.setGeometry(100, 100, 800, 600)

        # Initialize the database
        initialize_database()

        # Main Container
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize UI
        self.init_ui()

    def init_ui(self):
        # Create the main layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # Add Sidebar
        self.create_sidebar()

        # Add Stacked Widget for Content
        self.content_area = QStackedWidget()
        self.main_layout.addWidget(self.content_area)

        # Add Dashboard as Default View
        self.dashboard_view = QLabel("Welcome to the Dashboard!")
        self.dashboard_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_area.addWidget(self.dashboard_view)

    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.Box)
        sidebar_layout = QVBoxLayout(sidebar)

        # Navigation Buttons
        btn_dashboard = QPushButton("Dashboard")
        btn_dashboard.clicked.connect(lambda: self.switch_view(self.dashboard_view))

        btn_users = QPushButton("Users")
        btn_users.clicked.connect(self.display_users)

        btn_payments = QPushButton("Payments")
        btn_payments.clicked.connect(self.display_payments)

        btn_bills = QPushButton("Bills")
        btn_bills.clicked.connect(self.display_bills)

        btn_add_user = QPushButton("Add User")
        btn_add_user.clicked.connect(self.add_user)

        btn_add_payment = QPushButton("Add Payment")
        btn_add_payment.clicked.connect(self.add_payment)

        btn_add_bill = QPushButton("Add Bill")
        btn_add_bill.clicked.connect(self.add_bill)

        # Add buttons to the layout
        for button in [btn_dashboard, btn_users, btn_payments, btn_bills, btn_add_user, btn_add_payment, btn_add_bill]:
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()
        self.main_layout.addWidget(sidebar)

        # Apply styling to sidebar
        sidebar.setStyleSheet("""
            QPushButton {
                background-color: lightblue;
                font-size: 14px;
                border: none;
                padding: 10px;
                margin: 5px 0;
            }
            QPushButton:hover {
                background-color: skyblue;
            }
            QFrame {
                background-color: #f7f9fc;
                border: 1px solid #d1d9e6;
            }
        """)

    def switch_view(self, widget):
        self.content_area.setCurrentWidget(widget)

    def add_user(self):
        add_user_widget = QWidget()
        layout = QVBoxLayout()

        lbl_name = QLabel("Name:")
        txt_name = QLineEdit()

        lbl_email = QLabel("Email:")
        txt_email = QLineEdit()

        lbl_debts = QLabel("Debts:")
        txt_debts = QLineEdit()

        lbl_aptNo = QLabel("Apartment No:")
        txt_aptNo = QLineEdit()

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(
            lambda: self.save_user(txt_name.text(), txt_email.text(), txt_debts.text(), txt_aptNo.text())
        )

        layout.addWidget(lbl_name)
        layout.addWidget(txt_name)
        layout.addWidget(lbl_email)
        layout.addWidget(txt_email)
        layout.addWidget(lbl_debts)
        layout.addWidget(txt_debts)
        layout.addWidget(lbl_aptNo)
        layout.addWidget(txt_aptNo)
        layout.addWidget(btn_save)

        add_user_widget.setLayout(layout)
        self.content_area.addWidget(add_user_widget)
        self.switch_view(add_user_widget)

    def save_user(self, name, email, debts, aptNo):
        if not name or not email or not debts or not aptNo:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            execute_query(
                "INSERT INTO User (name, email, debts, aptNo) VALUES (?, ?, ?, ?)",
                (name, email, float(debts), int(aptNo))
            )
            QMessageBox.information(self, "Success", "User added successfully.")
            self.display_users()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Debts and Apartment No must be numeric.")

    def display_users(self):
        rows = execute_query("SELECT * FROM User")
        if rows is None:
            return

        table = QTableWidget()
        table.setRowCount(len(rows))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["User ID", "Name", "Email", "Debts", "Apartment No"])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.switch_view(self.dashboard_view))

        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        self.content_area.addWidget(container)
        self.switch_view(container)

    def add_payment(self):
        add_payment_widget = QWidget()
        layout = QVBoxLayout()

        lbl_amount = QLabel("Amount:")
        txt_amount = QLineEdit()

        lbl_date = QLabel("Date:")
        txt_date = QLineEdit()

        lbl_bill_id = QLabel("Bill ID:")
        txt_bill_id = QLineEdit()

        btn_save = QPushButton("Save Payment")
        btn_save.clicked.connect(
            lambda: self.save_payment(txt_amount.text(), txt_date.text(), txt_bill_id.text())
        )

        layout.addWidget(lbl_amount)
        layout.addWidget(txt_amount)
        layout.addWidget(lbl_date)
        layout.addWidget(txt_date)
        layout.addWidget(lbl_bill_id)
        layout.addWidget(txt_bill_id)
        layout.addWidget(btn_save)

        add_payment_widget.setLayout(layout)
        self.content_area.addWidget(add_payment_widget)
        self.switch_view(add_payment_widget)

    def save_payment(self, amount, date, bill_id):
        if not amount or not date or not bill_id:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            execute_query(
                "INSERT INTO Payments (amount, date, bill_id) VALUES (?, ?, ?)",
                (float(amount), date, int(bill_id))
            )
            QMessageBox.information(self, "Success", "Payment added successfully.")
            self.display_payments()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount and Bill ID must be numeric.")

    def display_payments(self):
        rows = execute_query("SELECT Payments.id, Payments.amount, Payments.date, Bill.details FROM Payments JOIN Bill ON Payments.bill_id = Bill.bill_id")
        if rows is None:
            return

        table = QTableWidget()
        table.setRowCount(len(rows))
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Payment ID", "Amount", "Date", "Bill Details"])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.switch_view(self.dashboard_view))

        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        self.content_area.addWidget(container)
        self.switch_view(container)

    def add_bill(self):
        add_bill_widget = QWidget()
        layout = QVBoxLayout()

        lbl_amount = QLabel("Amount:")
        txt_amount = QLineEdit()

        lbl_due_date = QLabel("Due Date:")
        txt_due_date = QLineEdit()

        lbl_details = QLabel("Details:")
        txt_details = QLineEdit()

        lbl_user_id = QLabel("User ID:")
        txt_user_id = QLineEdit()

        btn_save = QPushButton("Save Bill")
        btn_save.clicked.connect(
            lambda: self.save_bill(txt_amount.text(), txt_due_date.text(), txt_details.text(), txt_user_id.text())
        )

        layout.addWidget(lbl_amount)
        layout.addWidget(txt_amount)
        layout.addWidget(lbl_due_date)
        layout.addWidget(txt_due_date)
        layout.addWidget(lbl_details)
        layout.addWidget(txt_details)
        layout.addWidget(lbl_user_id)
        layout.addWidget(txt_user_id)
        layout.addWidget(btn_save)

        add_bill_widget.setLayout(layout)
        self.content_area.addWidget(add_bill_widget)
        self.switch_view(add_bill_widget)

    def save_bill(self, amount, due_date, details, user_id):
        if not amount or not due_date or not user_id:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            execute_query(
                "INSERT INTO Bill (amount, due_date, details, user_id) VALUES (?, ?, ?, ?)",
                (float(amount), due_date, details, int(user_id))
            )
            QMessageBox.information(self, "Success", "Bill added successfully.")
            self.display_bills()
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount and User ID must be numeric.")

    def display_bills(self):
        rows = execute_query("SELECT bill_id, amount, due_date, details, user_id FROM Bill")
        if rows is None:
            return

        table = QTableWidget()
        table.setRowCount(len(rows))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Bill ID", "Amount", "Due Date", "Details", "User ID"])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                table.setItem(i, j, QTableWidgetItem(str(value)))

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.switch_view(self.dashboard_view))

        layout = QVBoxLayout()
        layout.addWidget(table)
        layout.addWidget(back_button)

        container = QWidget()
        container.setLayout(layout)
        self.content_area.addWidget(container)
        self.switch_view(container)
if __name__ == "__main__":
    app = QApplication([])
    window = ApartmentManagementSystem()
    window.show()
    app.exec()