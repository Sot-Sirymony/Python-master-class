from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QComboBox, QPushButton, QWidget
from controllers.property_controller import add_room, fetch_properties

class AddRoomView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Room")
        self.layout = QVBoxLayout()

        properties = fetch_properties()

        self.property_selector = QComboBox()
        self.property_selector.addItems([prop[1] for prop in properties])

        self.name_input = QLineEdit("Enter Room Name/Number")
        self.type_input = QLineEdit("Enter Room Type (e.g., Single, Double)")
        self.size_input = QLineEdit("Enter Size (in sq ft or m²)")
        self.price_input = QLineEdit("Enter Rental Price")
        self.amenities_input = QLineEdit("Enter Amenities (comma-separated)")

        self.add_btn = QPushButton("Save Room")
        self.add_btn.clicked.connect(self.save_room)

        for widget in [self.property_selector, self.name_input, self.type_input, self.size_input, self.price_input, self.amenities_input, self.add_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def save_room(self):
        property_id = self.property_selector.currentIndex() + 1
        name = self.name_input.text()
        room_type = self.type_input.text()
        size = self.size_input.text()
        rental_price = self.price_input.text()
        amenities = self.amenities_input.text()
        try:
            add_room(property_id, name, room_type, size, rental_price, amenities)
            print("Room added successfully!")
            self.close()
        except Exception as e:
            print(f"Failed to add room: {e}")
