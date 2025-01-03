from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QStatusBar, QVBoxLayout,
    QSplitter, QTreeWidget, QTreeWidgetItem, QStackedWidget,
    QLabel, QLineEdit, QPushButton, QSizePolicy, QWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from utils.stylesheet_loader import load_stylesheet
from modules.room_management import RoomPropertyManagementUI  # Import your module


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set Window Properties
        self.setWindowTitle("Room Rental Management System")
        self.resize(1024, 768)

        # Initialize Room Management UI before sidebar
        self.room_property_management_ui = RoomPropertyManagementUI()

        # Sections Map
        self.sections = [
            "Dashboard", "Properties & Rooms", "Tenants", "Leases", 
            "Payments", "Bookings", "Reports"
        ]
        self.sidebar_action_map = {}

        # Initialize Layout Components
        self.init_toolbar()
        self.init_sidebar()
        self.init_main_content()
        self.init_footer()

        # Main Split Layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.main_content)
        splitter.setStretchFactor(1, 4)
        
        # Set Central Widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_dark_mode(self):
        if hasattr(self, "_dark_mode") and self._dark_mode:
            self.disable_dark_mode()
            self._dark_mode = False
        else:
            self.enable_dark_mode()
            self._dark_mode = True

    def enable_dark_mode(self):
        stylesheet = load_stylesheet(mode="dark_mode", subdirectory="main-layout")
        self.setStyleSheet(stylesheet)

    def disable_dark_mode(self):
        stylesheet = load_stylesheet(mode="light_mode", subdirectory="main-layout")
        self.setStyleSheet(stylesheet)

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        # Navigation Actions
        for section in self.sections:
            action = QAction(QIcon("placeholder.png"), section, self)
            action.triggered.connect(lambda checked, s=section: self.switch_module(s))
            toolbar.addAction(action)

        # Spacer to push search bar and buttons to the right
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        toolbar.addWidget(spacer)

        # Search Bar
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search...")
        search_bar.setFixedWidth(200)
        toolbar.addWidget(search_bar)

        # Notification and Settings Icons
        toolbar.addAction(QAction(QIcon("notification.png"), "Notifications", self))
        toolbar.addAction(QAction(QIcon("settings.png"), "Settings", self))

        # Dark Mode Toggle Button
        self.dark_mode_button = QPushButton("🌙 Dark Mode")
        self.dark_mode_button.setObjectName("darkModeButton")
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        toolbar.addWidget(self.dark_mode_button)

    def init_sidebar(self):
        self.sidebar = QTreeWidget()
        self.sidebar.setHeaderHidden(True)

        # Add Sidebar Items
        sections = {
            "Dashboard": [],
            "Properties & Rooms": [
                "Add Property", 
                "View Properties", 
                "Add Room", 
                "View Rooms"
            ],
            "Tenants": ["Add Tenant", "View Tenants"],
            "Payments": ["Record Payment", "Payment History"],
            "Reports": ["Rent Collection", "Occupancy Rates"]
        }

        for section, subsections in sections.items():
            parent_item = QTreeWidgetItem([section])
            for subsection in subsections:
                child_item = QTreeWidgetItem([subsection])
                parent_item.addChild(child_item)
                self.map_sidebar_action(subsection)
            self.sidebar.addTopLevelItem(parent_item)

        self.sidebar.itemClicked.connect(self.handle_sidebar_click)

    def map_sidebar_action(self, subsection):
        if subsection == "Add Property":
            self.sidebar_action_map[subsection] = self.room_property_management_ui.show_add_property_form
        elif subsection == "View Properties":
            self.sidebar_action_map[subsection] = self.room_property_management_ui.show_property_table
        elif subsection == "Add Room":
            self.sidebar_action_map[subsection] = self.room_property_management_ui.show_add_room_form
        elif subsection == "View Rooms":
            self.sidebar_action_map[subsection] = self.room_property_management_ui.show_room_table

    def handle_sidebar_click(self, item, column):
        section = item.text(column)

        if section in self.sidebar_action_map:
            self.sidebar_action_map[section]()
        elif section in self.sections:  # Handle parent sections
            print(f"Switched to parent section: {section}")
            if section == "Properties & Rooms":
                self.main_content.setCurrentWidget(self.room_property_management_ui)
        else:
            print(f"Unknown section: {section}")

    def init_main_content(self):
        self.main_content = QStackedWidget()

        # Add placeholders for other sections
        for section in self.sections:
            placeholder = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(QLabel(f"{section} Content Area"))
            placeholder.setLayout(layout)
            self.main_content.addWidget(placeholder)

        # Add Room and Property Management Module
        self.main_content.addWidget(self.room_property_management_ui)

    def init_footer(self):
        footer = QStatusBar()
        self.setStatusBar(footer)

        footer.addWidget(QLabel("Version 1.0"))
        footer.addWidget(QPushButton("Help"))
        footer.addWidget(QPushButton("Contact Support"))

    def switch_module(self, section):
        print(f"Switched to {section}")

    def load_dashboard_data(self):
        print("Loading dashboard data...")

    def load_payments_data(self):
        print("Loading payment data...")
