import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QTableWidget, QTableWidgetItem, QPushButton,QLabel, QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
import csv

class PropertyManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real Estate Property Manager")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Search bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search properties...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_properties)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # Property table
        self.property_table = QTableWidget()
        self.property_table.setColumnCount(3)
        self.property_table.setHorizontalHeaderLabels(["Property ID", "Name", "Location"])
        self.property_table.cellClicked.connect(self.display_property_details)
        main_layout.addWidget(self.property_table)

        # Property details
        self.detail_label = QLabel("Select a property to see details.")
        main_layout.addWidget(self.detail_label)

        self.setLayout(main_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("Add Property")
        add_button.clicked.connect(self.add_property)
        edit_button = QPushButton("Edit Property")
        edit_button.clicked.connect(self.edit_property)
        delete_button = QPushButton("Delete Property")
        delete_button.clicked.connect(self.delete_property)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.load_properties()

    def load_properties(self):
        self.properties = []
        try:
            with open('properties.csv', 'r') as file:
                reader = csv.reader(file)
                self.properties = list(reader)
        except FileNotFoundError:
            pass
        self.update_table()        

    def update_table(self):
        self.property_table.setRowCount(len(self.properties))
        for row_idx, property in enumerate(self.properties):
            for col_idx, item in enumerate(property):
                self.property_table.setItem(row_idx, col_idx, QTableWidgetItem(item))    

    def search_properties(self):
        search_term = self.search_input.text().lower()
        filtered_properties = [prop for prop in self.properties if search_term in prop[1].lower()]
        self.property_table.setRowCount(len(filtered_properties))
        for row_idx, property in enumerate(filtered_properties):
            for col_idx, item in enumerate(property):
                self.property_table.setItem(row_idx, col_idx, QTableWidgetItem(item))

    def display_property_details(self, row, column):
        property = self.properties[row]
        details = f"Property ID: {property[0]}\nName: {property[1]}\nLocation: {property[2]}"
        self.detail_label.setText(details)

    def add_property(self):
        dialog = PropertyDialog(self)
        if dialog.exec():
            new_property = dialog.get_data()
            self.properties.append(new_property)
            self.update_table()
            self.save_properties()

    def edit_property(self):
        current_row = self.property_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a property to edit.")
            return
        dialog = PropertyDialog(self, self.properties[current_row])
        if dialog.exec():
            updated_property = dialog.get_data()
            self.properties[current_row] = updated_property
            self.update_table()
            self.save_properties()
    
    
    def delete_property(self):
        current_row = self.property_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a property to delete.")
            return
        del self.properties[current_row]
        self.update_table()
        self.save_properties()

    def save_properties(self):
        with open('properties.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.properties)

class PropertyDialog(QDialog):
    def __init__(self, parent, property=None):
            super().__init__(parent)
            self.setWindowTitle("Property Details")
            self.property = property

            layout = QFormLayout()
            self.property_id_input = QLineEdit()
            self.name_input = QLineEdit()
            self.location_input = QLineEdit()

            layout.addRow("Property ID:", self.property_id_input)
            layout.addRow("Name:", self.name_input)
            layout.addRow("Location:", self.location_input)

            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)

            self.setLayout(layout)

            # This should be inside the __init__ method
            if property:
                self.property_id_input.setText(property[0])
                self.name_input.setText(property[1])
                self.location_input.setText(property[2])

    def get_data(self):
        return [
            self.property_id_input.text(),
            self.name_input.text(),
            self.location_input.text()
        ]    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    manager = PropertyManager()
    manager.show()
    sys.exit(app.exec())

                
