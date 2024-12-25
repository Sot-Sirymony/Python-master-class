from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QWidget
from controllers.property_controller import update_room

class EditRoomView(QWidget):
    def __init__(self, room_id, current_data):
        super().__init__()
        self.setWindowTitle("Edit Room")
        self.room_id = room_id
        self.layout = QVBoxLayout()

        # Pre-fill fields with current data
        self.name_input = QLineEdit(current_data['name'])
        self.type_input = QLineEdit(current_data['type'])
        self.size_input = QLineEdit(str(current_data['size']))
        self.price_input = QLineEdit(str(current_data['rental_price']))
        self.amenities_input = QLineEdit(current_data['amenities'])

        self.update_btn = QPushButton("Save Changes")
        self.update_btn.clicked.connect(self.save_changes)

        for widget in [self.name_input, self.type_input, self.size_input, self.price_input, self.amenities_input, self.update_btn]:
            self.layout.addWidget(widget)

        self.setLayout(self.layout)

    def save_changes(self):
        name = self.name_input.text()
        room_type = self.type_input.text()
        size = self.size_input.text()
        rental_price = self.price_input.text()
        amenities = self.amenities_input.text()
        try:
            update_room(self.room_id, name, room_type, size, rental_price, amenities)
            print("Room updated successfully!")
            self.close()
        except Exception as e:
            print(f"Failed to update room: {e}")
