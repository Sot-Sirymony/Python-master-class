
from utils.stylesheet_loader import load_stylesheet
from PyQt6.QtWidgets import QApplication
from layout.main_layout import MainWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # Load and apply stylesheet
    app.setStyleSheet(load_stylesheet(mode="base_mode", subdirectory="main-layout"))
    # Initialize and show the main window
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
