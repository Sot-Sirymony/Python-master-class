from PyQt6.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QDialog

class AddTenantView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Tenant")
        self.layout = QVBoxLayout()

        # Input Fields
        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        self.layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        self.layout.addWidget(self.last_name_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Phone")
        self.layout.addWidget(self.phone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.layout.addWidget(self.email_input)

        # Save Button
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_tenant)
        self.layout.addWidget(self.save_btn)

        self.setLayout(self.layout)

    def save_tenant(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # Call the controller to save the tenant
        from controllers.tenant_controller import add_tenant
        try:
            add_tenant(first_name, last_name, phone, email)
            print("Tenant added successfully!")
            self.accept()  # Close the dialog
        except Exception as e:
            print(f"Error adding tenant: {e}")
