import base64
import ctypes
import os
import sys

from PyQt6.QtGui import QIcon, QPixmap
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
    icon = QPixmap()
    icon.loadFromData(base64.b64decode(config.icon))
    application.setWindowIcon(QIcon(icon))
    # This statement is needed for the icon to show in the taskbar
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("stuttgart.DHBW.DatenbankenII.BBaum.1.0")

    # Create the MainWindow instance
    config.mainWindow = MainWindow()

    # change console window size
    os.system('mode con: cols=170 lines=40')

    # Execute the Application
    logger.info("Starting the application!")
    application.exec()


if __name__ == "__main__":
    main()
