## Step 3: Views

# File: views/rental_management_view.py
# from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QLabel
# from controllers.rental_management_controller import set_rental_price_and_terms, update_occupancy_status
# class RentalManagement(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Rental Management")
#         self.layout = QVBoxLayout()

#         # Filter Dropdown
#         self.filter_input = QComboBox()
#         self.filter_input.addItems(["All", "Available", "Rented", "Maintenance"])
#         self.filter_input.currentTextChanged.connect(self.filter_rooms)
#         self.layout.addWidget(self.filter_input)

#         # Room Table
#         self.room_table = QTableWidget()
#         self.room_table.setColumnCount(10)  # Updated to include the Tenant column and the Actions column
#         self.room_table.setHorizontalHeaderLabels([
#             "ID", "Name", "Type", "Rental Price", "Payment Frequency", 
#             "Security Deposit", "Grace Period", "Occupancy Status", "Tenant", "Actions"
#         ])
#         self.layout.addWidget(self.room_table)

#         # Buttons
#         self.refresh_btn = QPushButton("Refresh Rooms")
#         self.refresh_btn.clicked.connect(self.load_rooms)
#         self.layout.addWidget(self.refresh_btn)

#         self.setLayout(self.layout)
#         self.load_rooms()
#     def load_rooms(self):
#         from controllers.rental_management_controller import fetch_room_details
#         rooms = fetch_room_details()  # Fetch rooms with tenant data
#         self.room_table.setRowCount(0)

#         # Ensure the table has the correct number of columns including the Actions column
#         self.room_table.setColumnCount(10)  # Add one column for actions
#         self.room_table.setHorizontalHeaderLabels([
#             "ID", "Name", "Type", "Rental Price", "Payment Frequency", 
#             "Security Deposit", "Grace Period", "Occupancy Status", "Tenant", "Actions"
#         ])

#         for row_data in rooms:
#             row = self.room_table.rowCount()
#             self.room_table.insertRow(row)

#             # Populate standard columns
#             for col, data in enumerate(row_data):
#                 self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

#             # Add "Edit" button to the last column
#             edit_btn = QPushButton("Edit")
#             edit_btn.clicked.connect(lambda _, r=row_data: self.edit_room(r))
#             self.room_table.setCellWidget(row, 9, edit_btn)  # Actions column index is 9



#     # def edit_room(self, room_data):
#     #     print(f"Editing room: {room_data}")
#     def edit_room(self, room_data):
#         from views.edit_rental import EditRentalView
#         dialog = EditRentalView(room_data, self)
#         if dialog.exec():
#             print("Room details updated successfully.")
#             self.load_rooms()  # Refresh the table

#     # def filter_rooms(self, status):
#     #     # Logic to reload rooms based on filter
#     #     print(f"Filtering rooms by status: {status}")
#     def filter_rooms(self, status):
#         from controllers.rental_management_controller import fetch_room_details

#         # Fetch all rooms
#         all_rooms = fetch_room_details()

#         # Filter based on status if not "All"
#         if status != "All":
#             filtered_rooms = [room for room in all_rooms if room[7] == status]  # Room status is in column 7
#         else:
#             filtered_rooms = all_rooms

#         # Populate the table with filtered rooms
#         self.room_table.setRowCount(0)
#         for row_data in filtered_rooms:
#             row = self.room_table.rowCount()
#             self.room_table.insertRow(row)
#             for col, data in enumerate(row_data):
#                 self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

#             # Add Edit Button
#             edit_btn = QPushButton("Edit")
#             edit_btn.clicked.connect(lambda _, r=row_data: self.edit_room(r))
#             self.room_table.setCellWidget(row, 8, edit_btn)

from PyQt6.QtWidgets import QVBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QLabel
from views.edit_rental import EditRentalView  # Import the EditRentalView dialog
from controllers.rental_management_controller import fetch_room_details


class RentalManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rental Management")
        self.layout = QVBoxLayout()

        # Filter Dropdown
        self.filter_input = QComboBox()
        self.filter_input.addItems(["All", "Available", "Rented", "Maintenance"])
        self.filter_input.currentTextChanged.connect(self.filter_rooms)
        self.layout.addWidget(self.filter_input)

        # Room Table
        self.room_table = QTableWidget()
        self.room_table.setColumnCount(10)  # Adding an "Actions" column
        self.room_table.setHorizontalHeaderLabels([
            "ID", "Name", "Type", "Rental Price", "Payment Frequency", 
            "Security Deposit", "Grace Period", "Occupancy Status", 
            "Tenant", "Actions"
        ])
        self.layout.addWidget(self.room_table)

        # Buttons
        self.refresh_btn = QPushButton("Refresh Rooms")
        self.refresh_btn.clicked.connect(self.load_rooms)
        self.layout.addWidget(self.refresh_btn)

        self.setLayout(self.layout)
        self.load_rooms()

    def load_rooms(self):
        rooms = fetch_room_details()  # Fetch rooms with tenant data
        self.room_table.setRowCount(0)
        for row_data in rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)
            for col, data in enumerate(row_data):  # Populate all columns except actions
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
            self.room_table.setCellWidget(row, 9, edit_btn)

    def open_edit_view(self, room_data):
        dialog = EditRentalView(room_data, self)
        if dialog.exec():
            self.load_rooms()  # Refresh the table after editing

    def filter_rooms(self, status):
        all_rooms = fetch_room_details()
        filtered_rooms = all_rooms if status == "All" else [room for room in all_rooms if room[7] == status]
        self.room_table.setRowCount(0)
        for row_data in filtered_rooms:
            row = self.room_table.rowCount()
            self.room_table.insertRow(row)
            for col, data in enumerate(row_data):
                self.room_table.setItem(row, col, QTableWidgetItem(str(data)))

            # Add Edit Button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, r=row_data: self.open_edit_view(r))
            self.room_table.setCellWidget(row, 9, edit_btn)
