import sys

from PyQt6.QtWidgets import QApplication

from GUI import MainWindow


def main():
    application = QApplication(sys.argv)

    # Create the MainWindow instance
    mainWindow = MainWindow()

    # Execute the Application
    application.exec()


if __name__ == "__main__":
    main()
