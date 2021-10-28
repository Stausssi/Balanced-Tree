from functools import partial
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QSlider, QLineEdit, QVBoxLayout, QFrame

from .util import createHorizontalLayout, createVerticalLayout, displayUserMessage
from .Dialogs import DialogType, ConfirmationDialog

from util import readCSV
from config import DEFAULT_ORDER, QIntValidator_MAX


class MainWindow(QWidget):
    """
    This class represents the main window of the balanced tree application.
    """

    def __init__(self):
        super().__init__()

        # Configure the window
        self.setWindowTitle("Balancierter Baum")
        self.setGeometry(0, 0, 1280, 720)

        # Create the window layout
        self.setLayout(createVerticalLayout([self.__createTreeLayout(), self.__createFooter()]))

        # Other variables
        self.__scrollContent = ""
        self.__order = DEFAULT_ORDER

        # Show this window
        self.show()

    @staticmethod
    def __createTreeLayout() -> QVBoxLayout:
        """
        This method creates the tree layout of the application.

        Returns:
            QVBoxLayout: The layout of the tree.
        """

        temp = QLabel("Temporary main label")
        temp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return createVerticalLayout([temp])

    def __createFooter(self) -> QVBoxLayout:
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

        # Order input
        orderLabel = QLabel("Order")
        orderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        orderInput = QLineEdit()
        orderInput.setText(str(DEFAULT_ORDER))
        orderInput.setValidator(QIntValidator(1, QIntValidator_MAX))
        orderInput.returnPressed.connect(
            lambda: self.__showDialog(
                "Willst du die Ordnung wirklich verändern? Dadurch wird der komplette Baum zurückgesetzt.",
                partial(
                    self.__updateOrder,
                    int(orderInput.text())
                ),
                hasCancel=True,
                onFail=partial(
                    orderInput.setText,
                    str(self.__order)
                )
            ) if int(orderInput.text()) != self.__order else None
        )

        orderLayout = createVerticalLayout([orderLabel, orderInput])

        # Create the buttons
        button_insert = QPushButton("Insert")
        button_insert.clicked.connect(
            partial(
                self.__showDialog,
                "Welchen Eintrag möchtest du hinzufügen?",
                self.__insert,
                DialogType.INSERT
            )
        )

        button_find = QPushButton("Find")
        button_find.clicked.connect(
            partial(
                self.__showDialog,
                "Nach welchem Eintrag möchtest du suchen?",
                self.__search,
                DialogType.FIND
            )
        )

        button_delete = QPushButton("Delete")
        button_delete.clicked.connect(
            partial(
                self.__showDialog,
                "Welchen Eintrag möchtest du entfernen?",
                self.__delete,
                DialogType.DELETE
            )
        )

        button_csv = QPushButton("Import CSV")
        button_csv.clicked.connect(
            partial(
                self.__showDialog,
                "Wähle die CSV-Datei zum Importieren aus.",
                self.__showCSVContents,
                DialogType.CSV
            )
        )

        button_autofill = QPushButton("Auto fill")
        button_autofill.clicked.connect(
            partial(
                self.__showDialog,
                "Fülle die nachfolgenden Felder aus, um dem Baum zufällig zu befüllen.",
                self.__randomFill,
                DialogType.FILL
            )
        )

        button_reset = QPushButton("Reset")
        button_reset.clicked.connect(
            partial(
                self.__showDialog,
                "Willst du den Baum wirklich zurücksetzen?",
                self.__reset,
                DialogType.RESET,
                True
            )
        )

        # Combine the layouts
        configLayout = createHorizontalLayout([orderLayout, sliderLayout])
        configLayout.addStretch(0)

        operationLayout = createHorizontalLayout([button_insert, button_find, button_delete])
        operationLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        extendedOperationsLayout = createHorizontalLayout([button_csv, button_autofill, button_reset])
        extendedOperationsLayout.insertStretch(1, 1)
        extendedOperationsLayout.insertStretch(3, 1)
        extendedOperationsLayout.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout = createHorizontalLayout([
            configLayout, operationLayout, extendedOperationsLayout
        ])

        # Make every layout the same size
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        layout.setStretch(2, 1)

        # Use a frame to display a horizontal line
        hLine = QFrame()
        hLine.setFrameShape(QFrame.Shape.HLine)

        return createVerticalLayout([hLine, layout])

    def __showDialog(self, text, callback, dialogType=DialogType.NONE, hasCancel=False, onFail=None) -> None:
        """
        This method creates and shows a dialog. On success, callback will be called.

        Args:
            text (str): The text the dialog should display.
            callback (Callable): A callback, which will be called if the user confirms the dialog.
            dialogType (DialogType): The messageType of dialog. This will determine the layout of the dialog.
            hasCancel (bool): Whether the dialog should have a cancel button
            onFail (Callable or None): The callback to execute on cancellation of the dialog.

        Returns:
            None: Nothing
        """

        dialog = ConfirmationDialog(text, self, dialogType, hasCancel)

        if dialog.exec():
            callback(*dialog.getReturnValues())
        elif onFail is not None:
            onFail()

    # ---------- [Callback functions] ---------- #

    def __updateOrder(self, value) -> None:
        """
        This method is called after the user updates the order of the tree.

        Args:
            value (int): The new order of the tree

        Returns:
            None: Nothing
        """

        self.__order = int(value)
        self.__reset()

    def __insert(self, value) -> None:
        """
        This method is used to insert a value into the tree. It is used as a dialog-callback.

        Args:
            value (int): The new value

        Returns:
            None: Nothing
        """

        # TODO: Implementieren
        print("Insert:", value)
        pass

    def __search(self, value) -> None:
        """
        This method is used to search for a value in the tree. It is used as a dialog-callback.

        Args:
            value (int): The value to search for

        Returns:
            None: Nothing
        """

        # TODO: Implementieren
        print("Search:", value)
        pass

    def __delete(self, value) -> None:
        """
        This method is used to remove a value from the tree. It is used as a dialog-callback.

        Args:
            value (int): The value which will be deleted.

        Returns:
            None: Nothing
        """

        # TODO: Implementieren
        print("Delete:", value)
        pass

    def __showCSVContents(self, path) -> None:
        """
        This method displays the contents of a given CSV-file. It is used as a dialog-callback.

        Args:
            path (str): The path to the CSV-file

        Returns:
            None: Nothing
        """

        try:
            self.__scrollContent = readCSV(path)

            self.__showDialog(
                "Hier eine Übersicht über die Einträge der Datei:", self.__importCSVContents, DialogType.SCROLL_CONTENT,
                True
            )
        except FileNotFoundError as e:
            displayUserMessage("reading CSV file", e)

    def __importCSVContents(self) -> None:
        """
        This method imports the data from a previously read CSV-file. It is used as a dialog-callback.
        NOTE: This method also resets the string containing the scroll contents. Therefore, calling getScrollContents()
        after this method will return an empty string.

        Returns:
            None: Nothing
        """

        invalidLines: dict[int, str] = {}
        lineCount = 1

        # Create a list of lists containing the operation as the first element and the value as the second
        for operation, *value in [line.replace(" ", "").split(",") for line in self.__scrollContent.split("\n")]:
            # Check whether the value is singular
            if len(value) == 1:
                value = value[0]

                # Match the operation
                match operation.lower():
                    case "i":
                        try:
                            # Insert the value
                            print(operation, "Insert value", value)
                        except ValueError as e:
                            # Add line to invalid lines
                            invalidLines.update({
                                lineCount: str(e)
                            })
                    case "d":
                        try:
                            # Delete the value
                            print(operation, "delete value", value)
                        except ValueError as e:
                            # Add line to invalid lines
                            invalidLines.update({
                                lineCount: str(e)
                            })
                    case _:
                        # Add line to invalid lines
                        invalidLines.update({
                            lineCount: f"Invalid operation '{operation}'!"
                        })
            else:
                # Add line to invalid lines
                invalidLines.update({
                    lineCount: f"Invalid number of entries ({len(value)})!"
                })

            lineCount += 1

        if len(invalidLines) > 0:
            self.__scrollContent = "\n".join([f"{line}: {error}" for line, error in invalidLines.items()])

            self.__showDialog(
                "The following lines contain mistakes and couldn't be added",
                print,
                DialogType.SCROLL_CONTENT,
                False
            )

        # Reset scroll content
        self.__scrollContent = ""

    def __randomFill(self, lowerBorder, upperBorder, count) -> None:
        """
        This method randomly fills the tree with n entries between the given bounds. It is used as a dialog-callback.

        Args:
            lowerBorder (int): The lower border of the RNG.
            upperBorder (int): The upper border of the RNG.
            count (int): The number of elements, which will be added.

        Returns:
            None: Nothing
        """

        try:
            lowerBorder = int(lowerBorder)
            upperBorder = int(upperBorder)
            count = int(count)
        except ValueError as e:
            displayUserMessage("parsing user input", e)
            return

        # Check whether given params are actually possible
        if any([lowerBorder < 0, upperBorder < 0, count <= 0]):
            displayUserMessage("parsing user input", ValueError("Negative values are not allowed!"))
        elif lowerBorder > upperBorder:
            displayUserMessage("parsing user input", ValueError("Lower border is bigger than upper border"))
        elif count > upperBorder - lowerBorder + 1:
            displayUserMessage(
                "parsing user input",
                ValueError(f"Can't fit {count} values in the range [{lowerBorder}, {upperBorder}]")
            )
        else:
            # TODO: Implementieren
            print("Random fill:", lowerBorder, upperBorder, count)

    def __reset(self) -> None:
        """
        This method resets the tree. It is used as a dialog-callback.

        Returns:
            None: Nothing
        """

        # TODO: Implementieren
        print("reset")
        pass

    # ---------- [Public methods] ---------- #

    def getScrollContent(self) -> str:
        """
        This method returns a string representing the contents of the scroll view of the dialog.

        Returns:
            str: The contents of the scroll area
        """

        return self.__scrollContent
