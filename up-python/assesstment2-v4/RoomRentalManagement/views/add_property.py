from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget
from controllers.property_controller import add_property

class AddPropertyView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Property")
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit("Enter Property Name")
        self.address_input = QLineEdit("Enter Address")
        self.description_input = QTextEdit("Enter Description")
        self.amenities_input = QLineEdit("Enter Amenities (comma-separated)")

        self.add_btn = QPushButton("Save Property")
        self.add_btn.clicked.connect(self.save_property)

        for widget in [self.name_input, self.address_input, self.description_input, self.amenities_input, self.add_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def save_property(self):
        name = self.name_input.text()
        address = self.address_input.text()
        description = self.description_input.toPlainText()
        amenities = self.amenities_input.text()
        try:
            add_property(name, address, description, amenities)
            print("Property added successfully!")
            self.close()
        except Exception as e:
            print(f"Failed to add property: {e}")
