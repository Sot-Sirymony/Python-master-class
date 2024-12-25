from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget
from controllers.property_controller import update_property, fetch_properties

class EditPropertyView(QWidget):
    def __init__(self, property_id, current_data):
        super().__init__()
        self.setWindowTitle("Edit Property")
        self.property_id = property_id
        self.layout = QVBoxLayout()

        # Pre-fill fields with current data
        self.name_input = QLineEdit(current_data['name'])
        self.address_input = QLineEdit(current_data['address'])
        self.description_input = QTextEdit(current_data['description'])
        self.amenities_input = QLineEdit(current_data['amenities'])

        self.update_btn = QPushButton("Save Changes")
        self.update_btn.clicked.connect(self.save_changes)

        for widget in [self.name_input, self.address_input, self.description_input, self.amenities_input, self.update_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def save_changes(self):
        name = self.name_input.text()
        address = self.address_input.text()
        description = self.description_input.toPlainText()
        amenities = self.amenities_input.text()
        try:
            update_property(self.property_id, name, address, description, amenities)
            print("Property updated successfully!")
            self.close()
        except Exception as e:
            print(f"Failed to update property: {e}")
