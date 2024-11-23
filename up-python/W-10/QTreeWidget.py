import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QDialog, QFormLayout, QLineEdit,
    QDialogButtonBox, QMessageBox, QTreeWidget, QTreeWidgetItem
)
from PyQt6.QtGui import QFont


class TreeWidgetExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTreeWidget Example")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        # Left block for QTreeWidget
        self.tree_widget = QTreeWidget()
        font = QFont("Khmer OS", 11)
        self.tree_widget.setFont(font)
        self.tree_widget.setHeaderLabels(["Item"])
        main_layout.addWidget(self.tree_widget)

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

        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def show_add_dialog(self):
        dialog = ItemDialog(self)
        if dialog.exec():
            new_item_text = dialog.get_item_text()
            if new_item_text:
                selected_item = self.tree_widget.currentItem()
                if selected_item:
                    QTreeWidgetItem(selected_item, [new_item_text])
                else:
                    QTreeWidgetItem(self.tree_widget, [new_item_text])

    def remove_item(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            parent_item = selected_item.parent()
            if parent_item:
                parent_item.removeChild(selected_item)
            else:
                index = self.tree_widget.indexOfTopLevelItem(selected_item)
                self.tree_widget.takeTopLevelItem(index)

    def show_modify_dialog(self):
        selected_item = self.tree_widget.currentItem()
        if selected_item:
            dialog = ItemDialog(self, selected_item.text(0))
            if dialog.exec():
                modified_text = dialog.get_item_text()
                if modified_text:
                    selected_item.setText(0, modified_text)
        else:
            QMessageBox.warning(self, "No Selection", "Please select an item to modify.")


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
    window = TreeWidgetExample()
    window.show()
    sys.exit(app.exec())
    button_layout.addStretch()
    main_layout.addLayout(button_layout)

    self.setLayout(main_layout)

    def show_add_dialog(self):
        dialog = ItemDialog(self)
        if dialog.exec():
            new_item_text = dialog.get_item_text()
            if new_item_text:
                current_item = self.tree_widget.currentItem()
                if current_item:
                    new_item = QTreeWidgetItem(current_item, [new_item_text])
                    current_item.addChild(new_item)
                else:
                    new_item = QTreeWidgetItem([new_item_text])
                    self.tree_widget.addTopLevelItem(new_item)

    def show_modify_dialog(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to modify.")
            return
        current_item_text = current_item.text(0)
        dialog = ItemDialog(self, current_item_text)
        if dialog.exec():
            modified_item_text = dialog.get_item_text()
            if modified_item_text:
                current_item.setText(0, modified_item_text)
        
    def remove_item(self):
        current_item = self.tree_widget.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return
        parent_item = current_item.parent()
        if parent_item:
            parent_item.removeChild(current_item)
        else:
            index = self.tree_widget.indexOfTopLevelItem(current_item)
            self.tree_widget.takeTopLevelItem(index)


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
        window = TreeWidgetExample()
        window.show()
        sys.exit(app.exec())
        # Left block for QTreeWidget
        self.tree_widget = QTreeWidget()
        font = QFont("Khmer OS", 11)
        self.tree_widget.setFont(font)
        self.tree_widget.setHeaderLabels(["Item"])
        self.tree_widget.itemSelectionChanged.connect(self.item_selected)
        main_layout.addWidget(self.tree_widget)

        # Selected Item Label
        self.selected_label = QLabel("Selected Item: None")
        self.selected_label.setFont(font)
        button_layout.addWidget(self.selected_label)

        def item_selected(self):
            selected_items = self.tree_widget.selectedItems()
            if selected_items:
                selected_text = selected_items[0].text(0)
                self.selected_label.setText(f"Selected Item: {selected_text}")
            else:
                self.selected_label.setText("Selected Item: None")
