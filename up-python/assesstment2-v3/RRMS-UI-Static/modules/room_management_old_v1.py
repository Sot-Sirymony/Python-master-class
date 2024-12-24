from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton,
    QLabel, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt


class RoomPropertyManagementUI(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        self.main_layout = QVBoxLayout()
        self.current_section = None  # To track the current active section
        self.init_ui()

        # Set Layout
        self.setLayout(self.main_layout)

    def init_ui(self):
        self.show_property_table()  # Default view: Properties list

    def clear_layout(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # Section: Add Property
    def show_add_property_form(self):
        self.clear_layout()
        property_group = QGroupBox("Add Property")
        property_layout = QFormLayout()

        self.property_name_input = QLineEdit()
        self.property_location_input = QLineEdit()
        self.property_description_input = QTextEdit()
        self.property_amenities_input = QComboBox()
        self.property_amenities_input.addItems(["Wi-Fi", "Parking", "Pool"])

        property_layout.addRow("Property Name:", self.property_name_input)
        property_layout.addRow("Location:", self.property_location_input)
        property_layout.addRow("Description:", self.property_description_input)
        property_layout.addRow("Amenities:", self.property_amenities_input)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Property")
        save_button.clicked.connect(self.save_property)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.show_property_table)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        property_layout.addRow(button_layout)

        property_group.setLayout(property_layout)
        self.main_layout.addWidget(property_group)

    # Section: Add Room
    def show_add_room_form(self):
        self.clear_layout()
        room_group = QGroupBox("Add Room")
        room_layout = QFormLayout()

        self.room_number_input = QLineEdit()
        self.room_type_input = QComboBox()
        self.room_type_input.addItems(["Single", "Double", "Suite"])
        self.room_size_input = QLineEdit()
        self.room_rental_price_input = QLineEdit()
        self.room_amenities_input = QComboBox()
        self.room_amenities_input.addItems(["AC", "TV", "Ensuite Bathroom"])

        room_layout.addRow("Room Number:", self.room_number_input)
        room_layout.addRow("Type:", self.room_type_input)
        room_layout.addRow("Size:", self.room_size_input)
        room_layout.addRow("Rental Price:", self.room_rental_price_input)
        room_layout.addRow("Amenities:", self.room_amenities_input)

        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Room")
        save_button.clicked.connect(self.save_room)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.show_room_table)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        room_layout.addRow(button_layout)

        room_group.setLayout(room_layout)
        self.main_layout.addWidget(room_group)

    # Section: View Properties
    def show_property_table(self):
        self.clear_layout()
        properties_group = QGroupBox("Properties List")
        properties_layout = QVBoxLayout()

        self.properties_table = QTableWidget(5, 3)
        self.properties_table.setHorizontalHeaderLabels(["Name", "Location", "Actions"])
        properties_layout.addWidget(self.properties_table)

        properties_group.setLayout(properties_layout)
        self.main_layout.addWidget(properties_group)

    # Section: View Rooms
    def show_room_table(self):
        self.clear_layout()
        rooms_group = QGroupBox("Rooms List")
        rooms_layout = QVBoxLayout()

        self.rooms_table = QTableWidget(5, 4)
        self.rooms_table.setHorizontalHeaderLabels(["Room", "Type", "Size", "Price"])
        rooms_layout.addWidget(self.rooms_table)

        rooms_group.setLayout(rooms_layout)
        self.main_layout.addWidget(rooms_group)

    # Save Property Action
    def save_property(self):
        QMessageBox.information(self, "Save Property", "Property saved successfully!")
        self.show_property_table()

    # Save Room Action
    def save_room(self):
        QMessageBox.information(self, "Save Room", "Room saved successfully!")
        self.show_room_table()
