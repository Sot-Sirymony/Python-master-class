import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QAction

class MenuBarExample(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menu Bar Example")
        self.setGeometry(100, 100, 600, 400)
        # Create the menu bar
        menu_bar = self.menuBar()

        # Create File menu
        file_menu = menu_bar.addMenu("File")
        # Create actions for the File menu
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)  # Connect the Exit action to close the application

        # Add actions to the File menu
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Add a separator line
        file_menu.addAction(exit_action)
        # Create Edit menu
        edit_menu = menu_bar.addMenu("Edit")

        # Create actions for the Edit menu
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        # Add actions to the Edit menu
        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuBarExample()
    window.show()
    sys.exit(app.exec())
        
