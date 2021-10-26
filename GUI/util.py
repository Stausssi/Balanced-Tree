from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget


def createVerticalLayout(widgets) -> QVBoxLayout:
    """
    This method creates a vertical layout by appending each widget of the given widgets.

    Args:
        widgets (list[QWidget]): A list of PyQt widgets

    Returns:
        QVBoxLayout: The created layout
    """

    layout = QVBoxLayout()

    for widget in widgets:
        layout.addWidget(widget)

    return layout


def createHorizontalLayout(widgets) -> QHBoxLayout:
    """
    This method creates a horizontal layout by appending each widget of the given widgets.

    Args:
        widgets (list[QWidget]): A list of PyQt widgets

    Returns:
        QHBoxLayout: The created layout
    """

    layout = QHBoxLayout()

    for widget in widgets:
        layout.addWidget(widget)

    return layout
