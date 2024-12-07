import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMenu
from PyQt6.QtGui import QAction, QContextMenuEvent

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text Editor with Context Menu")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.create_context_menu()

    def create_context_menu(self):
        self.cut_action = QAction("Cut", self)
        self.cut_action.triggered.connect(self.text_edit.cut)

        self.copy_action = QAction("Copy", self)
        self.copy_action.triggered.connect(self.text_edit.copy)

        self.paste_action = QAction("Paste", self)
        self.paste_action.triggered.connect(self.text_edit.paste)

        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete_text)

    def delete_text(self):
        cursor = self.text_edit.textCursor()
        cursor.removeSelectedText()

    def contextMenuEvent(self, event: QContextMenuEvent):
        context_menu = QMenu(self)
        context_menu.addAction(self.cut_action)
        context_menu.addAction(self.copy_action)
        context_menu.addAction(self.paste_action)
        context_menu.addAction(self.delete_action)
        context_menu.exec(event.globalPos())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())        
        


