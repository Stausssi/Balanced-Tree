import ctypes
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from loguru import logger

import config
from GUI import MainWindow


@logger.catch
def main():
    # create logging file

    if config.LOGGING:
        logger.add("logs/{time}.log", rotation="1 MB")
    else:
        logger.disable("")

    application = QApplication(sys.argv)
    application.setApplicationName("Balancierter Baum")
    application.setStyle("Fusion")

    # Icon from: https://icons8.com/icon/47388/hierarchy"
    application.setWindowIcon(QIcon("GUI/icon.png"))
    # This statement is needed for the icon to show in the taskbar
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("stuttgart.DHBW.DatenbankenII.BBaum.1.0")

    # Create the MainWindow instance
    config.mainWindow = MainWindow()

    # Execute the Application
    logger.info("Starting the application!")
    application.exec()


if __name__ == "__main__":
    main()
