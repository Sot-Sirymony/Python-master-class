from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog, QLabel

class EditTenantView(QDialog):
    def __init__(self, tenant_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Tenant Details")
        self.layout = QVBoxLayout()

        # Tenant Data
        self.tenant_id = tenant_data[0]  # Extract tenant ID
        self.layout.addWidget(QLabel(f"Editing Tenant: {tenant_data[1]}"))

        # Input Fields (Pre-filled)
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.first_name_input.setText(tenant_data[1].split(" ")[0])  # Assuming first name is first word
        self.layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.last_name_input.setText(tenant_data[1].split(" ")[-1])  # Assuming last name is last word
        self.layout.addWidget(self.last_name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.phone_input.setText(tenant_data[2])  # Pre-fill phone
        self.layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setText(tenant_data[3])  # Pre-fill email
        self.layout.addWidget(self.email_input)

        # Save Button
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_tenant)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_tenant(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # Call the controller to save changes
        from controllers.tenant_controller import update_tenant
        try:
            update_tenant(self.tenant_id, first_name, last_name, phone, email)
            print("Tenant updated successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            print(f"Failed to update tenant: {e}")
