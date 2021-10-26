from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget

from GUI import createHorizontalLayout, createVerticalLayout


class MainWindow(QWidget):
    """
    This class represents the main window of the balanced tree application.
    """

    def __init__(self):
        super().__init__()

        # Configure the window
        self.setWindowTitle("Balancierter Baum")
        self.setGeometry(0, 0, 1280, 720)

        # Create the main layout
        self.setLayout(createVerticalLayout([self.__createMainLayout(), self.__createFooter()]))

        # Show this window
        self.show()

    @staticmethod
    def __createMainLayout():
        """
        This method creates the tree layout of the application.

        Returns:
            Any: The layout of the tree.
        """

        temp = QLabel("Temporary main label")
        temp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return createVerticalLayout([temp])

    @staticmethod
    def __createFooter():
        """
        This method creates the footer layout containing buttons for each operation.

        Returns:
            QHBoxLayout: The layout containing the buttons
        """

        # Create the widgets
        button_insert = QPushButton("Insert")
        button_insert.clicked.connect(lambda _: print("Open insert dialog"))
        button_delete = QPushButton("Delete")
        button_delete.clicked.connect(lambda _: print("Open delete dialog"))

        # Combine the layout
        layout = createHorizontalLayout([button_insert, button_delete])

        # Add spacing
        layout.insertStretch(0, 2)
        layout.insertStretch(3, 2)

        return layout
