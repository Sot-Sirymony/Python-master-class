
from PyQt6.QtCore import Qt
#from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QDockWidget
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QVBoxLayout, QWidget, QPushButton, QDockWidget, QHeaderView
)
from views.dashboard import Dashboard  # Main dashboard
from views.property_room import PropertyRoomManagement
from views.rental_management import RentalManagement
from views.tenant import TenantManagement
from views.payment import PaymentManagement
from views.dashboard import Dashboard  # Reports view
from PyQt6.QtWidgets import QHeaderView
from views.tenant_management import TenantManagement  # Import the TenantManagement view

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Room Rental Management System")
        self.setGeometry(100, 100, 1200, 800)

        # Main Layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        # Initialize Views
        self.dashboard = Dashboard()
        self.property_room_management = PropertyRoomManagement()
        self.tenant_management = TenantManagement()
        self.rental_management =RentalManagement()
        self.payment_management = PaymentManagement()
        self.reports = Dashboard()

        # Add Views to Stack
        self.central_widget.addWidget(self.dashboard)
        self.central_widget.addWidget(self.property_room_management)
        self.central_widget.addWidget(self.tenant_management)
        self.central_widget.addWidget(self.rental_management)
        self.central_widget.addWidget(self.payment_management)
        self.central_widget.addWidget(self.reports)

        # Sidebar Navigation
        self.init_sidebar()

    def init_sidebar(self):
        sidebar = QDockWidget("Navigation", self)
        container = QWidget()
        layout = QVBoxLayout()

        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.dashboard))

        property_room_btn = QPushButton("Properties & Rooms")
        property_room_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.property_room_management))
        
        tenant_btn = QPushButton("Tenants")
        tenant_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.tenant_management))
        
        rental_btn = QPushButton("Rental Management")
        rental_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.rental_management))

        payment_btn = QPushButton("Payments")
        payment_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.payment_management))

        reports_btn = QPushButton("Reports")
        reports_btn.clicked.connect(lambda: self.central_widget.setCurrentWidget(self.reports))

        for btn in [dashboard_btn, property_room_btn,rental_btn, tenant_btn, payment_btn, reports_btn]:
            layout.addWidget(btn)

        container.setLayout(layout)
        sidebar.setWidget(container)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sidebar)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

