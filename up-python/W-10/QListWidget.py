import sys
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout,QTableWidget, QTableWidgetItem, QPushButton,QLabel, QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QMessageBox
# import csv

# import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QDialog, QFormLayout, QLineEdit, 
    QDialogButtonBox, QMessageBox, QListWidget, QLabel
)
from PyQt6.QtGui import QFont


class ListWidgetExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QListWidget Example")
        self.setGeometry(100, 100, 400, 200)

        main_layout = QHBoxLayout()

        # Left block for QListWidget
        self.list_widget = QListWidget()
        font = QFont("Khmer OS", 11)
        self.list_widget.setFont(font)
        self.list_widget.itemSelectionChanged.connect(self.item_selected)
        main_layout.addWidget(self.list_widget)

        # Right block for buttons
        button_layout = QVBoxLayout()

        self.add_button = QPushButton("Add Item")
        self.add_button.setFont(font)
        self.add_button.clicked.connect(self.show_add_dialog)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.setFont(font)
        self.remove_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_button)

        self.modify_button = QPushButton("Modify Item")
        self.modify_button.setFont(font)
        self.modify_button.clicked.connect(self.show_modify_dialog)
        button_layout.addWidget(self.modify_button)

        self.selected_item_label = QLabel("Selected Item: None")
        self.selected_item_label.setFont(font)
        button_layout.addWidget(self.selected_item_label)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def show_add_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Item")
        form_layout = QFormLayout(dialog)
        line_edit = QLineEdit()
        form_layout.addRow("Item:", line_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        form_layout.addWidget(button_box)

        def on_accept():
            item_text = line_edit.text()
            if item_text:
                self.list_widget.addItem(item_text)
                dialog.accept()

        button_box.accepted.connect(on_accept)
        button_box.rejected.connect(dialog.reject)
        dialog.exec()

    def remove_item(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            self.list_widget.takeItem(self.list_widget.row(selected_item))
        else:
            QMessageBox.warning(self, "Warning", "No item selected!")

    def show_modify_dialog(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            dialog = QDialog(self)
        self.selected_label = QLabel("Selected Item: None")
        self.selected_label.setFont(font)
        button_layout.addWidget(self.selected_label)

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        def item_selected(self):
            selected_items = self.list_widget.selectedItems()
            if selected_items:
                selected_text = selected_items[0].text()
                self.selected_label.setText(f"Selected Item: {selected_text}")
            else:
                self.selected_label.setText("Selected Item: None")

        def show_add_dialog(self):
            dialog = ItemDialog(self)
            if dialog.exec():
                new_item = dialog.get_item_text()
                if new_item:
                    self.list_widget.addItem(new_item)

        def show_modify_dialog(self):
            current_row = self.list_widget.currentRow()
            if current_row == -1:
                QMessageBox.warning(self, "No Selection", "Please select an item to modify.")
                return
            current_item = self.list_widget.item(current_row).text()
            dialog = ItemDialog(self, current_item)
            if dialog.exec():
                modified_item = dialog.get_item_text()
                if modified_item:
                    self.list_widget.item(current_row).setText(modified_item)
        def remove_item(self):
            current_row = self.list_widget.currentRow()
            if current_row != -1:
                self.list_widget.takeItem(current_row)

        class ItemDialog(QDialog):
            def __init__(self, parent=None, item_text=""):
                super().__init__(parent)
                self.setWindowTitle("Item Details")

                layout = QFormLayout()
                self.item_input = QLineEdit(item_text)
                font = QFont("Khmer OS", 11)
                self.item_input.setFont(font)
                layout.addRow("Item:", self.item_input)

                button_box = QDialogButtonBox(
                    QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
                )
                button_box.accepted.connect(self.accept)
                button_box.rejected.connect(self.reject)
                layout.addWidget(button_box)

                self.setLayout(layout)

            def get_item_text(self):
                return self.item_input.text()


        if __name__ == "__main__":
            app = QApplication(sys.argv)
            window = ListWidgetExample()
            window.show()
            sys.exit(app.exec())
                            
                            
                    
