import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLayout, QMessageBox


def createVerticalLayout(items) -> QVBoxLayout:
    """
    This method creates a vertical layout by appending each widget of the given items.

    Args:
        items (list[QWidget] or list[QLayout]): A list of PyQt widgets or layouts

    Returns:
        QVBoxLayout: The created layout
    """

    layout = QVBoxLayout()

    for item in items:
        if isinstance(item, QWidget):
            layout.addWidget(item)
        else:
            layout.addLayout(item)

    return layout


def createHorizontalLayout(items) -> QHBoxLayout:
    """
    This method creates a horizontal layout by appending each widget of the given items.

    Args:
        items (list[QWidget] or list[QLayout]): A list of PyQt widgets or layouts

    Returns:
        QHBoxLayout: The created layout
    """

    layout = QHBoxLayout()

    for item in items:
        if isinstance(item, QWidget):
            layout.addWidget(item)
        else:
            layout.addLayout(item)

    return layout


def displayUserMessage(message, error=None, fatal=False) -> int:
    """
    This method displays a message to the user with a given text, type and an optional error message.

    Args:
        message (str): The text of the message.
        error (None or Exception): The error message.
        fatal (bool): Whether the error was fatal and the application should quit.

    Returns:
        int: The return code of the message dialog.
    """

    messageBox = QMessageBox()
    messageBox.setText(message)
    messageBox.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
    messageBox.setWindowTitle("Benachrichtigung")
    messageBox.setIcon(QMessageBox.Icon.Information)

    if error:
        messageBox.setText(f"Something went wrong while {message}: {error}")
        messageBox.setIcon(QMessageBox.Icon.Warning)

        title = ""
        if fatal:
            messageBox.setIcon(QMessageBox.Icon.Critical)
            title = "Fatal "

        messageBox.setWindowTitle(title + "Error")

    result = messageBox.exec()

    if fatal:
        sys.exit(-1)

    return result


def clearLayout(layout):
    """
    This method clears the given layout of all widgets and layouts.

    Args:
        layout (QLayout): The layout to clear.

    Returns:
        None: Nothing
    """

    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
            # noinspection PyTypeChecker
            item.widget().setParent(None)
        elif item.layout():
            clearLayout(item.layout())
