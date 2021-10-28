from functools import partial

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QSlider, QLineEdit, QVBoxLayout, QFrame

from GUI import createHorizontalLayout, createVerticalLayout, DialogType, ConfirmationDialog


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
        self.__csvContent = ""

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
        orderInput.setValidator(QIntValidator())
        orderInput.editingFinished.connect(lambda: print("Order of the tree updated"))
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

    def __showDialog(self, text, callback, dialogType=DialogType.NONE, hasCancel=False) -> None:
        """
        This method creates and shows a dialog. On success, callback will be called.

        Args:
            text (str): The text the dialog should display.
            callback (def): A callback, which will be called if the user confirms the dialog.
            dialogType (DialogType): The type of dialog. This will determine the layout of the dialog.
            hasCancel (bool): Whether the dialog should have a cancel button

        Returns:
            None: Nothing
        """

        dialog = ConfirmationDialog(text, self, dialogType, hasCancel)

        if dialog.exec():
            callback(*dialog.getReturnValues())
        else:
            print("Dialog was cancelled")

    # ---------- [Callback functions] ---------- #

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

        # TODO: Implementieren
        print("CSV:", path)
        self.__csvContent = "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "lang\n" \
                            "text"

        self.__showDialog(
            "Hier eine Übersicht über die Einträge der Datei:", self.__importCSVContents, DialogType.CSV_OVERVIEW, True
        )

    def __importCSVContents(self) -> None:
        """
        This method imports the data from a previously read CSV-file. It is used as a dialog-callback.
        NOTE: This method also resets the string containing the CSV contents. Therefore, calling getCSVContents()
        after this method will return an empty string.

        Returns:
            None: Nothing
        """

        # TODO: Implementieren
        self.__csvContent = ""
        pass

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

        print("Random fill:", lowerBorder, upperBorder, count)
        # TODO: Implementieren
        pass

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

    def getCSVContent(self) -> str:
        """
        This method returns a string containing the content of a previously given CSV file.

        Returns:
            str: The contents of the file
        """

        return self.__csvContent
