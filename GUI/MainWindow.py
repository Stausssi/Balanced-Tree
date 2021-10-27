from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QSlider, QLineEdit, QVBoxLayout, QFrame

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
        self.setLayout(createVerticalLayout([self.__createTreeLayout(), self.__createFooter()]))

        self.__createOrderLayout()

        # Show this window
        self.show()

    @staticmethod
    def __createTreeLayout():
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
            QVBoxLayout: The layout containing the buttons
        """

        # Create the animation speed slider
        sliderLabel = QLabel("Animation speed: 1")
        sliderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setRange(1, 5)
        slider.setSingleStep(1)
        slider.valueChanged.connect(lambda value: sliderLabel.setText(f"Animation speed: {value}"))
        slider.sliderReleased.connect(lambda: print("slider released"))

        sliderLayout = createVerticalLayout([sliderLabel, slider])

        # Create the buttons
        button_autofill = QPushButton("Auto fill")
        button_autofill.clicked.connect(lambda _: print("Open autofill dialog"))

        button_insert = QPushButton("Insert")
        button_insert.clicked.connect(lambda _: print("Open insert dialog"))

        button_find = QPushButton("Find")
        button_find.clicked.connect(lambda _: print("Open find dialog"))

        button_delete = QPushButton("Delete")
        button_delete.clicked.connect(lambda _: print("Open delete dialog"))

        button_csv = QPushButton("Import CSV")
        button_csv.clicked.connect(lambda _: print("Open CSV dialog"))

        button_reset = QPushButton("Reset")
        button_reset.clicked.connect(lambda _: print("Reset the tree"))

        # Combine the layout
        layout = createHorizontalLayout([
            sliderLayout, button_autofill, button_insert, button_find, button_delete, button_csv, button_reset
        ])

        # Add spacing
        layout.insertStretch(1, 3)
        layout.insertStretch(3, 3)
        layout.insertStretch(5, 1)
        layout.insertStretch(7, 1)
        layout.insertStretch(9, 3)
        layout.insertStretch(11, 3)

        # Use a frame to display a horizontal line
        hLine = QFrame()
        hLine.setFrameShape(QFrame.Shape.HLine)

        return createVerticalLayout([hLine, layout])

    def __createOrderLayout(self):
        """

        Returns:

        """

        label = QLabel("Order")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        orderInput = QLineEdit()
        orderInput.setValidator(QIntValidator())

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setStyleSheet(".QFrame { border: 1px solid black; border-radius: 3px;}")
        frame.setGeometry(-2, -2, 250, 100)
        frame.setLayout(createVerticalLayout([label, orderInput]))
