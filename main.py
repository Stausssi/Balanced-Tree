import sys
import ctypes

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from GUI import MainWindow

mainWindow = None


def main():
    application = QApplication(sys.argv)
    application.setApplicationName("Balancierter Baum")
    application.setStyle("Fusion")

    # Icon from: https://icons8.com/icon/47388/hierarchy"
    application.setWindowIcon(QIcon("GUI/icon.png"))
    # This statement is needed for the icon to show in the taskbar
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("stuttgart.DHBW.DatenbankenII.BBaum.1.0")

    # Create the MainWindow instance
    global mainWindow
    mainWindow = MainWindow()

    # Execute the Application
    application.exec()


if __name__ == "__main__":
    main()
