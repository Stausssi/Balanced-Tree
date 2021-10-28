from enum import Enum, auto
from typing import Union

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QWidget, QLayout, QLineEdit, QPushButton, \
    QFormLayout, QFileDialog, QScrollArea

from GUI import createHorizontalLayout, createVerticalLayout


class DialogType(Enum):
    INSERT = auto()
    FIND = auto()
    DELETE = auto()

    CSV = auto()
    CSV_OVERVIEW = auto()
    FILL = auto()

    RESET = auto()
    NONE = auto()


class ConfirmationDialog(QDialog):
    """
    This class displays a dialog with a text, an optional layout and default buttons

    Args:
        text (str): The main text of the dialog.
        parent (QWidget): The parent of the widget. Usually the MainWindow.
        dialogType (DialogType): The type of the dialog. This will determine the inner layout of the dialog.
        hasCancel (bool): Whether the dialog should have an additional "Cancel" button
    """

    def __init__(self, text, parent, dialogType=DialogType.NONE, hasCancel=False):
        super().__init__(parent, Qt.WindowType.WindowCloseButtonHint)
        self.setModal(True)

        # Create the layout
        layout = QVBoxLayout()

        # Add the text label
        textLabel = QLabel(text)
        textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the buttons
        buttons = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox()
        if hasCancel:
            buttons |= QDialogButtonBox.StandardButton.Cancel
            self.buttonBox.rejected.connect(self.reject)

        self.buttonBox.setStandardButtons(buttons)
        self.buttonBox.accepted.connect(self.accept)

        # Disable the OK button by default
        self.okButton = self.buttonBox.button(QDialogButtonBox.StandardButton.Ok)

        if dialogType != DialogType.NONE and dialogType != DialogType.RESET and dialogType != DialogType.CSV_OVERVIEW:
            self.okButton.setEnabled(False)

        # Combine text, layout and buttons
        self.innerLayout = self.__getInnerLayout(dialogType)

        layout.addWidget(textLabel)
        layout.addLayout(self.innerLayout)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

    def __getInnerLayout(self, dialogType) -> Union[QLayout, None]:
        """
        This method returns the layout of the given DialogType.

        Args:
            dialogType (DialogType): The type of the dialog

        Returns:
            QLayout or None: The inner layout of the dialog.
        """

        match dialogType:
            case DialogType.INSERT | DialogType.FIND | DialogType.DELETE:
                # Create a layout containing a singular number input
                numInput = QLineEdit()
                numInput.setValidator(QIntValidator())
                numInput.textChanged.connect(self.__updateButtonEnabled)

                return createVerticalLayout([numInput])
            case DialogType.CSV:
                # Create a layout containing a text box and a button to open a file picker
                pathInput = QLineEdit()
                pathInput.setEnabled(False)
                pathInput.textChanged.connect(self.__updateButtonEnabled)

                pathButton = QPushButton()
                pathButton.setText("...")
                pathButton.clicked.connect(
                    lambda _: pathInput.setText(
                        QFileDialog.getOpenFileName(self, "Select a CSV file...", filter="CSV files (*.csv)")[0]
                    )
                )

                return createHorizontalLayout([pathInput, pathButton])
            case DialogType.CSV_OVERVIEW:
                # Create a layout containing a scroll view, which will be filled with the contents of the CSV file
                from GUI import MainWindow
                if isinstance(self.parent(), MainWindow):
                    text = QLabel(self.parent().getCSVContent())
                    text.setWordWrap(True)

                    scrollView = QScrollArea()
                    scrollView.setWidget(text)
                    return createVerticalLayout([scrollView])
            case DialogType.FILL:
                # Create a layout with three number inputs for the lower border, upper border and count of random items
                layout = QFormLayout()

                lowerBorder = QLineEdit()
                lowerBorder.setValidator(QIntValidator())
                lowerBorder.textChanged.connect(self.__updateButtonEnabled)

                upperBorder = QLineEdit()
                upperBorder.setValidator(QIntValidator())
                upperBorder.textChanged.connect(self.__updateButtonEnabled)

                count = QLineEdit()
                count.setValidator(QIntValidator())
                count.textChanged.connect(self.__updateButtonEnabled)

                layout.addRow("Untergrenze", lowerBorder)
                layout.addRow("Obergrenze", upperBorder)
                layout.addRow("Anzahl", count)

                return layout
            case DialogType.RESET | DialogType.NONE:
                # Create an empty layout
                return QVBoxLayout()

    def __updateButtonEnabled(self, *_) -> None:
        """
        This method updates the enabled status of a button by checking whether every input field has a valid value.
        ATTENTION: EVERY PARAM GIVEN TO THIS METHOD WILL BE VOIDED BY _

        Returns:
            None: Nothing
        """

        self.okButton.setEnabled(all([
            widget.hasAcceptableInput() for widget in self.__getInputWidgets() if isinstance(widget, QLineEdit)
        ]))

    def __getInputWidgets(self) -> list[QWidget]:
        """
        This method returns every input widget of this dialog.

        Returns:
            list[QWidget]: A list of widgets.
        """

        return [self.innerLayout.itemAt(i).widget() for i in range(self.innerLayout.count())]

    def getReturnValues(self) -> list[str]:
        """
        This method returns the values of every input field.

        Returns:
            list[str]: A list containing the value of every widget as a string
        """

        return [widget.text() for widget in self.__getInputWidgets() if isinstance(widget, QLineEdit)]