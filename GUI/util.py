from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QLayout


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
