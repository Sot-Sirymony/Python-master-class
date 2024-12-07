import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QToolBar, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor with Toolbar")
        self.setGeometry(100, 100, 600, 400)

        # Create the text edit widget
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # Track current file path
        self.current_file = None

        # Create the toolbar
        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Create actions
        new_action = QAction(QIcon("icons/new.png"), "New", self)
        new_action.setStatusTip("Create a new document")
        new_action.triggered.connect(self.new_file)
        new_action.setShortcut("Ctrl+N")

        open_action = QAction(QIcon("icons/open.png"), "Open", self)
        open_action.setStatusTip("Open an existing document")
        open_action.triggered.connect(self.open_file)
        open_action.setShortcut("Ctrl+O")

        save_action = QAction(QIcon("icons/save.png"), "Save", self)
        save_action.setStatusTip("Save the current document")
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut("Ctrl+S")

        cut_action = QAction(QIcon("icons/cut.png"), "Cut", self)
        cut_action.setStatusTip("Cut the selected text")
        cut_action.triggered.connect(self.text_edit.cut)
        cut_action.setShortcut("Ctrl+X")

        copy_action = QAction(QIcon("icons/copy.png"), "Copy", self)
        copy_action.setStatusTip("Copy the selected text")
        copy_action.triggered.connect(self.text_edit.copy)
        copy_action.setShortcut("Ctrl+C")

        paste_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        paste_action.setStatusTip("Paste text from clipboard")
        paste_action.triggered.connect(self.text_edit.paste)
        paste_action.setShortcut("Ctrl+V")

        # Add actions to the toolbar
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()
        toolbar.addAction(cut_action)
        toolbar.addAction(copy_action)
        toolbar.addAction(paste_action)

    def new_file(self):
        # Prompt to save unsaved changes
        if not self.confirm_save():
            return
        self.text_edit.clear()
        self.current_file = None
        self.setWindowTitle("Text Editor with Toolbar - New File")

    def open_file(self):
        # Prompt to save unsaved changes
        if not self.confirm_save():
            return
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.text_edit.setText(file.read())
                self.current_file = file_path
                self.setWindowTitle(f"Text Editor with Toolbar - {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {str(e)}")

    def save_file(self):
        if self.current_file is None:
            self.save_file_as()
        else:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.current_file = file_path
            self.save_file()

    def confirm_save(self):
        if not self.text_edit.document().isModified():
            return True
        reply = QMessageBox.question(
            self, "Save Changes",
            "The document has unsaved changes. Do you want to save them?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.save_file()
            return True
        elif reply == QMessageBox.StandardButton.No:
            return True
        else:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())
