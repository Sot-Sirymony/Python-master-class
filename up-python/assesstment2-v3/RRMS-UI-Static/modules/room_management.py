# from utils.stylesheet_loader import load_stylesheet
# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
#     QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton,
#     QLabel, QGroupBox, QMessageBox, QSizePolicy, QHeaderView
# )
# from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QTextEdit, QTableWidget, QTableWidgetItem, QPushButton,
    QLabel, QGroupBox, QMessageBox, QSizePolicy, QHeaderView
)
from PyQt6.QtCore import Qt
from functools import partial  # Import partial for connecting lambdas with parameters
from utils.stylesheet_loader import load_stylesheet

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
    # def load_table_stylesheet(self):
    #     stylesheet = load_stylesheet(mode="room_management", subdirectory="room-management")
    #     self.setStyleSheet(stylesheet)
    def load_table_stylesheet(self):
        stylesheet = load_stylesheet(mode="room_management", subdirectory="room-management")
        self.setStyleSheet(stylesheet)         
    def show_add_property_form(self):
        self.clear_layout()
        property_group = QGroupBox("Add Property")
        property_layout = QFormLayout()

        # Create input fields
        self.property_name_input = QLineEdit()
        self.property_location_input = QLineEdit()
        self.property_description_input = QTextEdit()
        self.property_amenities_input = QComboBox()
        self.property_amenities_input.addItems(["Wi-Fi", "Parking", "Pool"])

        # Add fields to the form
        property_layout.addRow("Property Name:", self.property_name_input)
        property_layout.addRow("Location:", self.property_location_input)
        property_layout.addRow("Description:", self.property_description_input)
        property_layout.addRow("Amenities:", self.property_amenities_input)

        # Add Save/Cancel buttons
        self.button_layout = QHBoxLayout()  # Store button layout for later access
        self.save_button = QPushButton("Save Property")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.show_property_table)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(cancel_button)

        # Add button layout to the form layout
        property_layout.addRow(self.button_layout)
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

    def show_property_table(self):
        self.clear_layout()
        properties_group = QGroupBox("Properties List")
        properties_layout = QVBoxLayout()

        self.properties_table = QTableWidget(5, 4)  # Add an extra column for Actions
        self.properties_table.setHorizontalHeaderLabels(["Name", "Location", "Amenities", "Actions"])

        for row in range(5):  # Replace with actual data fetching logic
            self.properties_table.setItem(row, 0, QTableWidgetItem(f"Property {row + 1}"))
            self.properties_table.setItem(row, 1, QTableWidgetItem("Location Placeholder"))
            self.properties_table.setItem(row, 2, QTableWidgetItem("Amenities Placeholder"))

            # Add Edit/Delete Buttons
            action_layout = QHBoxLayout()
            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")

            # Style buttons
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QPushButton:pressed {
                    background-color: #003f6b;
                }
            """)
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #d9534f;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c9302c;
                }
                QPushButton:pressed {
                    background-color: #ac2925;
                }
            """)

            # Connect buttons to actions
            edit_button.clicked.connect(lambda _, r=row: self.edit_property(r))
            delete_button.clicked.connect(lambda _, r=row: self.delete_property(r))

            # Add buttons to the action layout
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            # Wrap the layout in a QWidget
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            action_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            self.properties_table.setCellWidget(row, 3, action_widget)

        # Set table header and row policies to stretch
        header = self.properties_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        vertical_header = self.properties_table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set the table to fill its parent widget
        self.properties_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add table to the group and layout
        properties_layout.addWidget(self.properties_table)
        properties_group.setLayout(properties_layout)
        self.main_layout.addWidget(properties_group)

        # Apply table-wide stylesheet
        self.properties_table.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #dcdcdc;
                font-size: 16px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #0078d4;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #005a9e;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
    def edit_property(self, row):
        """Edit a property based on the selected row."""
        self.clear_layout()
        self.show_add_property_form()

        # Populate form fields with existing data
        self.property_name_input.setText(self.properties_table.item(row, 0).text())
        self.property_location_input.setText(self.properties_table.item(row, 1).text())
        self.property_amenities_input.setCurrentText(self.properties_table.item(row, 2).text())

        # Update Save button behavior
        if hasattr(self, "button_layout") and self.button_layout:
            # Clear existing buttons in the layout
            for i in reversed(range(self.button_layout.count())):
                self.button_layout.itemAt(i).widget().deleteLater()

            # Add new Save button for update
            update_button = QPushButton("Update Property")
            update_button.clicked.connect(lambda: self.update_property(row))
            self.button_layout.addWidget(update_button)

            # Add Cancel button
            cancel_button = QPushButton("Cancel")
            cancel_button.clicked.connect(self.show_property_table)
            self.button_layout.addWidget(cancel_button)
        else:
            print("Button layout not found!")
    def show_add_property_form(self):
        self.clear_layout()
        property_group = QGroupBox("Add Property")
        property_layout = QFormLayout()

        # Create input fields
        self.property_name_input = QLineEdit()
        self.property_location_input = QLineEdit()
        self.property_description_input = QTextEdit()
        self.property_amenities_input = QComboBox()
        self.property_amenities_input.addItems(["Wi-Fi", "Parking", "Pool"])

        # Add fields to the form
        property_layout.addRow("Property Name:", self.property_name_input)
        property_layout.addRow("Location:", self.property_location_input)
        property_layout.addRow("Description:", self.property_description_input)
        property_layout.addRow("Amenities:", self.property_amenities_input)

        # Add Save/Cancel buttons
        self.button_layout = QHBoxLayout()  # Store button layout for later access
        self.save_button = QPushButton("Save Property")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.show_property_table)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(cancel_button)

        # Add button layout to the form layout
        property_layout.addRow(self.button_layout)
        property_group.setLayout(property_layout)
        self.main_layout.addWidget(property_group)
 
    def edit_property(self, row):
        """Edit a property based on the selected row."""
        self.clear_layout()
        self.show_add_property_form()

        # Populate form fields with existing data
        self.property_name_input.setText(self.properties_table.item(row, 0).text())
        self.property_location_input.setText(self.properties_table.item(row, 1).text())
        self.property_amenities_input.setCurrentText(self.properties_table.item(row, 2).text())

        # Update Save button behavior
        property_group = self.main_layout.itemAt(0).widget()  # Fetch the QGroupBox
        if isinstance(property_group, QGroupBox):
            layout = property_group.layout()
            if layout and layout.itemAt(4):  # Ensure the button layout exists
                button_layout = layout.itemAt(4).layout()

                # Remove old buttons
                for i in reversed(range(button_layout.count())):
                    button_layout.itemAt(i).widget().deleteLater()

                # Recreate and add the updated Save button
                save_button = QPushButton("Update Property")
                save_button.clicked.connect(lambda: self.update_property(row))
                button_layout.addWidget(save_button)

                # Add Cancel button
    

    def update_property(self, row):
        # Retrieve data from input fields
        updated_name = self.property_name_input.text()
        updated_location = self.property_location_input.text()
        updated_amenities = self.property_amenities_input.currentText()

        # Validate that mandatory fields are not empty
        if not updated_name or not updated_location:
            QMessageBox.warning(self, "Validation Error", "Property Name and Location cannot be empty.")
            return

        # Update the table widget with new values
        self.properties_table.setItem(row, 0, QTableWidgetItem(updated_name))
        self.properties_table.setItem(row, 1, QTableWidgetItem(updated_location))
        self.properties_table.setItem(row, 2, QTableWidgetItem(updated_amenities))

        # Show success message
        QMessageBox.information(self, "Update Property", f"Property {row + 1} updated successfully!")

        # Return to the properties table view
        self.show_property_table()


    # Section: Delete Property
    def delete_property(self, row):
        reply = QMessageBox.question(self, "Delete Property",
                                     f"Are you sure you want to delete Property {row + 1}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Delete Property", f"Property {row + 1} deleted successfully!")
            self.show_property_table()
    def delete_property(self, row):
        reply = QMessageBox.question(
            self,
            "Delete Property",
            f"Are you sure you want to delete Property {row + 1}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Remove the specified row from the properties table
            self.properties_table.removeRow(row)

            # Show success message
            QMessageBox.information(self, "Delete Property", f"Property {row + 1} deleted successfully!")

            # Optional: Re-index the property rows or perform additional cleanup if necessary
            self.refresh_table()

    def refresh_table(self):
        """
        Optionally refresh or re-index the table rows after a deletion.
        """
        for row in range(self.properties_table.rowCount()):
            item = self.properties_table.item(row, 0)
            if item:
                item.setText(f"Property {row + 1}")        

    def show_room_table(self):
        self.clear_layout()
        rooms_group = QGroupBox("Rooms List")
        rooms_layout = QVBoxLayout()

        # Create the table widget
        self.rooms_table = QTableWidget(5, 5)  # Add an extra column for Actions
        self.rooms_table.setHorizontalHeaderLabels(["Room", "Type", "Size", "Price", "Actions"])

        for row in range(5):  # Replace with actual data fetching logic
            self.rooms_table.setItem(row, 0, QTableWidgetItem(f"Room {row + 1}"))
            self.rooms_table.setItem(row, 1, QTableWidgetItem("Type Placeholder"))
            self.rooms_table.setItem(row, 2, QTableWidgetItem("Size Placeholder"))
            self.rooms_table.setItem(row, 3, QTableWidgetItem("Price Placeholder"))

            # Add Edit/Delete Buttons
            action_layout = QHBoxLayout()
            edit_button = QPushButton("Edit")
            delete_button = QPushButton("Delete")

            # Style buttons
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #005a9e;
                }
                QPushButton:pressed {
                    background-color: #003f6b;
                }
            """)
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: #d9534f;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c9302c;
                }
                QPushButton:pressed {
                    background-color: #ac2925;
                }
            """)

            # Connect buttons to actions
            edit_button.clicked.connect(partial(self.edit_room, row))
            delete_button.clicked.connect(partial(self.delete_room, row))

            # Add buttons to the action layout
            action_layout.addWidget(edit_button)
            action_layout.addWidget(delete_button)

            # Wrap the layout in a QWidget
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            action_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

            # Add the action widget to the last column
            self.rooms_table.setCellWidget(row, 4, action_widget)

        # Configure headers
        header = self.rooms_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        vertical_header = self.rooms_table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Set the table to fill its parent widget
        self.rooms_table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Add table to the group and layout
        rooms_layout.addWidget(self.rooms_table)
        rooms_group.setLayout(rooms_layout)
        self.main_layout.addWidget(rooms_group)

        # Apply table-wide stylesheet
        self.rooms_table.setStyleSheet("""
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #dcdcdc;
                font-size: 16px;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #0078d4;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                border: 1px solid #005a9e;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)

    def edit_room(self, row):
        # Clear the current layout and show the Add Room form
        self.clear_layout()
        self.show_add_room_form()

        # Verify that the required input fields exist
        if hasattr(self, 'room_number_input') and hasattr(self, 'room_type_input'):
            # Populate form fields with existing data
            self.room_number_input.setText(self.rooms_table.item(row, 0).text())
            self.room_type_input.setCurrentText(self.rooms_table.item(row, 1).text())
            self.room_size_input.setText(self.rooms_table.item(row, 2).text())
            self.room_rental_price_input.setText(self.rooms_table.item(row, 3).text())

            # Update the Save button to behave as an Update button
            if hasattr(self, 'save_button'):
                self.save_button.setText("Update Room")
                self.disconnect_save_button()
                self.save_button.clicked.connect(lambda: self.update_room(row))
            else:
                print("Save button not found!")
        else:
            print("Input fields for editing a room are not initialized!")
    def disconnect_save_button(self):
        """Safely disconnect all signals from the save button."""
        if hasattr(self, 'save_button') and self.save_button:
            try:
                while self.save_button.receivers(self.save_button.clicked) > 0:
                    self.save_button.clicked.disconnect()
            except TypeError:
                pass  # Ignore errors if no connections exist
        
    def show_add_room_form(self):
        self.clear_layout()
        room_group = QGroupBox("Add/Edit Room")
        room_layout = QFormLayout()

        # Create input fields
        self.room_number_input = QLineEdit()
        self.room_type_input = QComboBox()
        self.room_type_input.addItems(["Single", "Double", "Suite"])
        self.room_size_input = QLineEdit()
        self.room_rental_price_input = QLineEdit()

        # Add fields to the form
        room_layout.addRow("Room Number:", self.room_number_input)
        room_layout.addRow("Type:", self.room_type_input)
        room_layout.addRow("Size:", self.room_size_input)
        room_layout.addRow("Rental Price:", self.room_rental_price_input)

        # Add Save/Cancel buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Room")
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.show_room_table)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(cancel_button)

        room_layout.addRow(button_layout)

        room_group.setLayout(room_layout)
        self.main_layout.addWidget(room_group)        

    def update_room(self, row):
        QMessageBox.information(self, "Update Room", f"Room {row + 1} updated successfully!")
        self.show_room_table()

    def delete_room(self, row):
        reply = QMessageBox.question(self, "Delete Room",
                                    f"Are you sure you want to delete Room {row + 1}?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Delete Room", f"Room {row + 1} deleted successfully!")
            self.show_room_table()         
    # Save Property Action
    def save_property(self):
        QMessageBox.information(self, "Save Property", "Property saved successfully!")
        self.show_property_table()

    # Save Room Action
    def save_room(self):
        QMessageBox.information(self, "Save Room", "Room saved successfully!")
        self.show_room_table()
