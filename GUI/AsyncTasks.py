import random
from enum import Enum, auto

from PyQt6.QtCore import pyqtSignal, QThread


class WorkerType(Enum):
    INSERT = auto()
    DELETE = auto()
    RANGE_INSERT = auto()


class AsyncWorker(QThread):
    """
    Base class for asynchronous operations.

    Args:
        mainWindow (MainWindow): The main window widget
        animationSpeed (int): The speed of the animation
        workerType (WorkerType): The type of the worker
        values (list[int]): The values to insert/delete. In case of workerType RANGE_INSERT, the first element of the
            list will be the lowerBorder, the second the upperBorder and the third the count.
    """

    finished = pyqtSignal()
    error = pyqtSignal(Exception)
    refresh = pyqtSignal()

    def __init__(self, mainWindow, animationSpeed, workerType, values):
        super().__init__(mainWindow)
        self.__tree = mainWindow.getTree()
        self._animationSpeed = animationSpeed
        self.__workerType = workerType
        self.__values = values

    def run(self) -> None:
        """
        This method asynchronously manipulates the tree.

        Returns:
            None: Nothing
        """

        try:
            match self.__workerType:
                case WorkerType.INSERT:
                    for value in self.__values:
                        self.__tree.insert(value)
                        self.refresh.emit()

                        self.msleep(1000 // self._animationSpeed)
                case WorkerType.DELETE:
                    for value in self.__values:
                        self.__tree.delete(value)
                        self.refresh.emit()

                        self.msleep(1000 // self._animationSpeed)
                case WorkerType.RANGE_INSERT:
                    try:
                        lower = self.__values[0]
                        upper = self.__values[1]
                        count = self.__values[2]
                    except IndexError as e:
                        print(e)
                        self.finished.emit()
                        return

                    while count > 0:
                        self.__tree.insert(random.randint(lower, upper))

                        self.refresh.emit()
                        self.msleep(1000 // self._animationSpeed)

                        count -= 1
        except ValueError as e:
            self.error.emit(e)

        self.finished.emit()

    def updateAnimationSpeed(self, newSpeed) -> None:
        """
        This method updates the animation speed.

        Args:
            newSpeed (int): The new speed

        Returns:
            None: Nothing
        """

        self._animationSpeed = newSpeed
