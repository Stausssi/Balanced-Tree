from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel

from GUI import createHorizontalLayout, createVerticalLayout


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configure the window
        self.setWindowTitle("Balancierter Baum")

        layouts = []
        self.setLayout(self.__createFooter())

        # Show this window
        self.show()

    def __createMainLayout(self):
        """

        Returns:

        """

        pass

    def __createFooter(self):
        """

        Returns:

        """


        button = QPushButton("Insert", self)

        return createHorizontalLayout([button])


