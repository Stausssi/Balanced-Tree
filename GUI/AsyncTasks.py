import random

from PyQt6.QtCore import pyqtSignal, QThread


class AsyncWorker(QThread):
    """
    Base class for asynchronous operations.

    Args:
        mainWindow (MainWindow): The main window widget
        animationSpeed (int): The speed of the animation
        operations (list[tuple[str, int]]): The values to insert/delete. In case of random insert, this list of tuples
            consists of "lower", "upper" and "count" with the corresponding values. Otherwise, only "i" and "d" are
            allowed operations.
    """

    finished = pyqtSignal(list)
    refresh = pyqtSignal()

    def __init__(self, mainWindow, animationSpeed, operations):
        super().__init__(mainWindow)
        self.__tree = mainWindow.getTree()
        self._animationSpeed = animationSpeed
        self.__operations = operations

    def run(self) -> None:
        """
        This method asynchronously manipulates the tree.

        Returns:
            None: Nothing
        """

        errorList: list[Exception] = []

        # Check whether random insert is desired
        if all([string in [tup[0] for tup in self.__operations] for string in ["lower", "upper", "count"]]):
            try:
                lower = int([operation[1] for operation in self.__operations if operation[0] == "lower"][0])
                upper = int([operation[1] for operation in self.__operations if operation[0] == "upper"][0])
                count = int([operation[1] for operation in self.__operations if operation[0] == "count"][0])

                while count > 0:
                    try:
                        self.__tree.insert(random.randint(lower, upper))

                        self.refresh.emit()
                        self.msleep(1000 // self._animationSpeed)

                        count -= 1
                    except ValueError:
                        # Ignore errors
                        pass
            except IndexError as e:
                errorList.append(e)
        else:
            entryCount = 0
            # Otherwise, go through operations and perform the operation
            for operation, value in self.__operations:
                try:
                    entryCount += 1

                    # Check if value is an int, or a list of the length 1 with 1 digit inside
                    if isinstance(value, int) or len(value) == 1 and value[0].isdigit():
                        if not isinstance(value, int):
                            value = int(value[0])

                        match operation.lower():
                            case "i":
                                self.__tree.insert(value)
                            case "d":
                                self.__tree.delete(value)
                            case _:
                                raise ValueError(f"Unknown operation '{operation}'!")

                        self.refresh.emit()
                        self.msleep(1000 // self._animationSpeed)
                    else:
                        raise ValueError(f"Invalid values: {value}")
                except Exception as e:
                    errorList.append(Exception(f"{entryCount}: {e}"))

        # Return the errors
        self.finished.emit(errorList)

    def updateAnimationSpeed(self, newSpeed) -> None:
        """
        This method updates the animation speed.

        Args:
            newSpeed (int): The new speed

        Returns:
            None: Nothing
        """

        self._animationSpeed = newSpeed
