import random
from time import sleep

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, QThread


class AsyncTask(QThread):
    """
    Base class for asynchronous operations.

    Args:
        mainWindow (MainWindow): The main window widget
        animationSpeed (int): The speed of the animation
    """

    finished = pyqtSignal()

    def __init__(self, mainWindow, animationSpeed):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
        self.animationSpeed = animationSpeed

    def run(self) -> None:
        self.finished.emit()


class AsyncRangeInsert(AsyncTask):
    """
    This class operates asynchronously to the main window and is used for insert animations.
    """

    insert = pyqtSignal(int)

    def __init__(self, mainWindow, animationSpeed, itemCount, lowerBorder, upperBorder):
        super().__init__(mainWindow, animationSpeed)
        self.itemCount = itemCount
        self.lowerBorder = lowerBorder
        self.upperBorder = upperBorder

    def run(self) -> None:
        """
        This method asynchronously inserts values into the tree.

        Returns:
            None: Nothing
        """

        while self.itemCount > 0:
            try:
                self.insert.emit(random.randint(self.lowerBorder, self.upperBorder))
                # self.mainWindow.insert(random.randint(self.lowerBorder, self.upperBorder), True)
                self.itemCount -= 1

                self.msleep(1000 // self.animationSpeed)
            except ValueError:
                pass

        super().run()


