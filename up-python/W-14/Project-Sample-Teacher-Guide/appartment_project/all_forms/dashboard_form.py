from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Database.dao import AccessDatabase


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Create the layout
        layout = QVBoxLayout()

        # Initialize figures and canvases for the plots
        self.figure1 = Figure()
        self.canvas1 = FigureCanvas(self.figure1)

        self.figure2 = Figure()
        self.canvas2 = FigureCanvas(self.figure2)

        self.figure3 = Figure()
        self.canvas3 = FigureCanvas(self.figure3)

        # Add canvases to the layout
        layout.addWidget(self.canvas1)
        layout.addWidget(self.canvas2)
        layout.addWidget(self.canvas3)

        self.setLayout(layout)

        # Generate the plots
        self.plot_bill_amounts()
        self.plot_payment_amounts()
        self.plot_users_debts()

    def plot_bill_amounts(self):
        """Plot a histogram of bill amounts."""
        try:
            self.figure1.clear()

            all_amounts = AccessDatabase().getAllBillAmounts()

            if not all_amounts:
                raise ValueError("No bill data available.")

            amounts = [row[0] for row in all_amounts]

            ax = self.figure1.add_subplot(111)
            ax.hist(amounts, bins=10, edgecolor='black')
            ax.set_xlabel('Amount')
            ax.set_ylabel('Frequency')
            ax.set_title('Distribution of Bill Amounts')

            self.canvas1.draw()
        except Exception as e:
            self.display_error_message(f"Error plotting bill amounts: {e}")

    def plot_payment_amounts(self):
        """Plot a histogram of payment amounts."""
        try:
            self.figure2.clear()

            all_amounts = AccessDatabase().getAllPaymentAmounts()

            if not all_amounts:
                raise ValueError("No payment data available.")

            amounts = [row[0] for row in all_amounts]

            ax = self.figure2.add_subplot(111)
            ax.hist(amounts, bins=10, edgecolor='black')
            ax.set_xlabel('Amount')
            ax.set_ylabel('Frequency')
            ax.set_title('Distribution of Payment Amounts')

            self.canvas2.draw()
        except Exception as e:
            self.display_error_message(f"Error plotting payment amounts: {e}")

    def plot_users_debts(self):
        """Plot a histogram of user debts."""
        try:
            self.figure3.clear()

            all_debts = AccessDatabase().getAllUsersDebts()

            if not all_debts:
                raise ValueError("No debt data available.")

            debts = [row[0] for row in all_debts]

            ax = self.figure3.add_subplot(111)
            ax.hist(debts, bins=10, edgecolor='black')
            ax.set_xlabel('Debt Amount')
            ax.set_ylabel('Frequency')
            ax.set_title('Distribution of User Debts')

            self.canvas3.draw()
        except Exception as e:
            self.display_error_message(f"Error plotting user debts: {e}")

    def display_error_message(self, message):
        """Display an error message box."""
        QMessageBox.critical(self, "Error", message)
