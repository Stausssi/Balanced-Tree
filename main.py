import sys

# from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from GUI import MainWindow


def main():
    application = QApplication(sys.argv)
    application.setApplicationName("Balancierter Baum")
    application.setStyle("Fusion")
    # application.setWindowIcon(QIcon("icon.svg"))

    # Create the MainWindow instance
    _ = MainWindow()

    # Execute the Application
    application.exec()


if __name__ == "__main__":
    main()
