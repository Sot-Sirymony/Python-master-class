import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QStatusBar, QLabel
from PyQt6.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor with Status Bar")
        self.setGeometry(100, 100, 600, 400)

        # Create the text edit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Create the status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Create labels for different sections in the status bar
        self.status_label = QLabel("Ready")
        self.cursor_label = QLabel("Line: 1, Column: 1")
        self.status_label.setStyleSheet("color: green;")
        self.cursor_label.setStyleSheet("font-weight: bold;")

        # Add labels to the status bar
        self.status_bar.addPermanentWidget(self.status_label, 1)
        self.status_bar.addPermanentWidget(self.cursor_label, 2)

        # Connect the cursor position change signal to update the cursor position
        self.text_edit.cursorPositionChanged.connect(self.update_cursor_position)
    def update_cursor_position(self):
        cursor = self.text_edit.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.cursor_label.setText(f"Line: {line}, Column: {column}")

    def show_temporary_message(self, message, duration=2000):
        self.status_bar.showMessage(message, duration)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())    

