import random
import sys
from functools import partial
from typing import Optional
from loguru import logger

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QPushButton, QLabel, QWidget, QSlider, QVBoxLayout, QFrame, QHBoxLayout, QSpinBox

from Tree import BalancedTree, Node
from config import DEFAULT_ORDER, QIntValidator_MAX
from util import readCSV
from .Dialogs import DialogType, ConfirmationDialog
from .GraphicalNode import GraphicalNode
from .util import createHorizontalLayout, createVerticalLayout, displayUserMessage, clearLayout


class MainWindow(QWidget):
    """
    This class represents the main window of the balanced tree application.
    """

    def __init__(self):
        super().__init__()

        # Variables
        self.__scrollContent = ""
        self.__order = DEFAULT_ORDER
        self.__animationSpeed = 1
        self.__tree = BalancedTree(self.__order)
        self.__enableAbleButtons: list[QPushButton] = []
        self.__graphicalNodes: dict[Node, GraphicalNode] = {}
        self.__searchNode: Optional[GraphicalNode] = None

        # Configure the window
        self.setWindowTitle("Balancierter Baum")
        self.setGeometry(0, 0, 1280, 720)

        # Create the layout
        self.__treeLayout = QVBoxLayout()

        self.setLayout(createVerticalLayout([self.__treeLayout, self.__createFooter()]))

        self.updateTreeLayout()

        # Show this window
        self.show()

    def updateTreeLayout(self) -> None:
        """
        This method updates the tree layout to show the given tree. Calling this function can be used to animate the
        tree.

        Returns:
            None: Nothing
        """

        # Basic list contains the root only
        nodes: list[list[Node]] = [[self.__tree.root]]
        layer = 1

        # Clear every item out of the layout
        clearLayout(self.__treeLayout)

        # This dict contains every graphical node of the tree
        self.__graphicalNodes = {}

        # This dict contains the parentInformation reference (QFrame) of every node
        references: dict[Node, tuple[QFrame, GraphicalNode]] = {
            self.__tree.root: (None, None)
        }

        # Construct the layout
        while len(nodes) > 0:
            # print(f"Layer {layer}: {[node.keys for node in nodes[0]]}")

            # Create a spacing row before the node
            self.__treeLayout.addLayout(QHBoxLayout(), 1)

            row = QHBoxLayout()
            row.setSpacing(0)

            # Create a new layer
            nodes.append([])
            for node in nodes[0]:
                # print(node)

                # Create a label containing the keys of the node
                row.addStretch(1)

                graphicalNode = GraphicalNode(
                    self.__order, node.keys, references.get(node)
                )

                # Save graphical node
                self.__graphicalNodes.update({
                    node: graphicalNode
                })

                row.addWidget(graphicalNode, 1)

                children = node.children
                if children:
                    # Add the children of the node to the next layer
                    nodes[1].extend(children)

                    for index, child in enumerate(children):
                        # print(f"{child} will connect to the {index}. reference")

                        references.update({
                            child: (graphicalNode.getReferences()[index], graphicalNode)
                        })

            row.addStretch(1)
            # print("----------------")

            # Add the row to the layout
            self.__treeLayout.addLayout(row)

            # Create a spacing row after the node
            self.__treeLayout.addLayout(QHBoxLayout(), 1)

            # Remove the old layer
            nodes = nodes[1:]

            # Remove empty layers
            for _ in range(nodes.count([])):
                nodes.remove([])

            layer += 1

        # print("\n\n")
        self.__updateEnableAbleButtons()

    def paintEvent(self, _) -> None:
        """
        This method is called every time the widget is painted. This is used to draw the connections between the
        GraphicalNodes.

        Args:
            _: The paint event. Not needed for this method

        Returns:
            None: Nothing
        """

        # Draw every connection
        painter = QPainter(self)
        for node in self.__graphicalNodes.values():
            if self.__searchNode == node:
                painter.setPen(QColor(0, 255, 0))
                painter.drawRect(self.__searchNode.geometry())
            else:
                painter.setPen(QColor(0, 0, 0))

            painter.drawLine(node.getLine())

    def __createFooter(self) -> QVBoxLayout:
        """
        This method creates the footer layout containing buttons for each operation.

        Returns:
            QVBoxLayout: The layout containing the buttons
        """

        # Order input
        orderLabel = QLabel("Order")
        orderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        orderInput = QSpinBox()
        orderInput.setRange(1, QIntValidator_MAX)
        orderInput.valueChanged.connect(self.__updateOrder)
        orderInput.setValue(DEFAULT_ORDER)

        orderLayout = createVerticalLayout([orderLabel, orderInput])

        # Create the animation speed slider
        sliderLabel = QLabel("Animation speed: 1")
        sliderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider = QSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.setRange(1, 5)
        slider.setSingleStep(1)
        slider.valueChanged.connect(lambda value: sliderLabel.setText(f"Animation speed: {value}"))
        slider.valueChanged.connect(self.__updateAnimationSpeed)

        sliderLayout = createVerticalLayout([sliderLabel, slider])

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
                True,
                None
            )
        )

        # Save buttons which can be disabled to list
        self.__enableAbleButtons = [button_find, button_delete, button_reset]

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

    def __updateEnableAbleButtons(self) -> None:
        """
        This method updated the enabled-state of the buttons, which can be en- or disabled.

        Returns:
            None: Nothing
        """

        for button in self.__enableAbleButtons:
            button.setEnabled(not self.__tree.isEmpty())

    # ---------- [Callback methods] ---------- #

    def __updateOrder(self, value) -> None:
        """
        This method is called after the user updates the order of the tree.

        Args:
            value (int): The new order of the tree

        Returns:
            None: Nothing
        """

        if value != self.__order:
            self.__order = int(value)

            # Get the current values of the tree
            values = self.__tree.getAllValues()

            # Create a new tree with the new order
            self.__tree = BalancedTree(self.__order)

            # logging
            logger.info(f"The order of the tree is changed to {value}")

            # Insert every of the old values into the new tree
            for value in values:
                try:
                    self.__insert(value, True)
                except ValueError as e:
                    print(e)

            # Trigger an update to remove artefacts (old connections)
            # TODO: Also update the window size -> This will also update the window size, if the user resized the window
            #  --> Therefore, don't reset the window size
            self.update()

    def __updateAnimationSpeed(self, value) -> None:
        """
        This method is called after the user updates the order the animation speed.

        Args:
            value (int): The new animation speed.

        Returns:
            None: Nothing
        """

        self.__animationSpeed = value

    def __insert(self, value, bulkInsert=False) -> None:
        """
        This method is used to insert a value into the tree. It is used as a dialog-callback.

        Args:
            value (int): The new value
            bulkInsert (bool): Whether a bulk of values is being inserted. This is true, if a CSV is imported.

        Returns:
            None: Nothing

        Raises:
            ValueError: If bulkInsert is true and the value couldn't be inserted into the tree.
        """

        try:
            # timer = QTimer(self)
            # timer.setInterval(1000 // self.__animationSpeed)
            # timer.setSingleShot(True)
            # timer.timeout.connect(timerCallback)
            # timer.start()
            logger.info(f"INSERT: {value}")

            self.__tree.insert(int(value))
            self.updateTreeLayout()

        except ValueError as e:
            if not bulkInsert:
                displayUserMessage("inserting value into the tree", e)
            else:
                raise e

    def __search(self, value) -> None:
        """
        This method is used to search for a value in the tree. It is used as a dialog-callback.

        Args:
            value (int): The value to search for

        Returns:
            None: Nothing
        """

        node, key = self.__tree.search(int(value))
        if key:
            displayUserMessage(f"{value} was found in the node {node}!")
        else:
            displayUserMessage(f"{value} couldn't be found! Last searched node: {node}")

    def __delete(self, value) -> None:
        """
        This method is used to remove a value from the tree. It is used as a dialog-callback.

        Args:
            value (int): The value which will be deleted.

        Returns:
            None: Nothing
        """

        logger.info(f"DELETE: {value}")
        self.__tree.delete(int(value))
        self.updateTreeLayout()

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
                            self.__insert(value, True)
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

        availableRange = upperBorder - lowerBorder + 1

        # Check whether given params are actually possible
        if any([lowerBorder < 0, upperBorder < 0, count <= 0]):
            displayUserMessage("parsing user input", ValueError("Negative values are not allowed!"))
        elif lowerBorder > upperBorder:
            displayUserMessage("parsing user input", ValueError("Lower border is bigger than upper border"))
        elif count > availableRange:
            displayUserMessage(
                "parsing user input",
                ValueError(f"Can't fit {count} values in the range [{lowerBorder}, {upperBorder}]")
            )
        else:
            # Get the existing keys
            existing_keys = [
                found for _, found in [
                    self.__tree.search(i) for i in range(lowerBorder, upperBorder + 1)
                ]
                if found
            ]

            # print(f"existing keys in the range [{lowerBorder}, {upperBorder}]: {existing_keys}")
            # Remove existing keys from availableRange
            availableRange -= len(existing_keys)

            # Check whether there are still enough values available
            if count > availableRange:
                displayUserMessage(
                    "parsing user input",
                    ValueError(
                        f"Can't fit {count} values in the range [{lowerBorder}, {upperBorder}], since {existing_keys} "
                        f"exist already!"
                    )
                )
            else:
                while count > 0:
                    try:
                        self.__insert(random.randint(lowerBorder, upperBorder), True)
                        count -= 1
                    except ValueError:
                        pass

    def __reset(self) -> None:
        """
        This method resets the tree. It is used as a dialog-callback.

        Returns:
            None: Nothing
        """

        self.__tree = BalancedTree(self.__order)
        self.updateTreeLayout()

    # ---------- [Public methods] ---------- #

    def getScrollContent(self) -> str:
        """
        This method returns a string representing the contents of the scroll view of the dialog.

        Returns:
            str: The contents of the scroll area
        """

        return self.__scrollContent

    def animateSearch(self, treeNode) -> None:
        """
        This method returns the corresponding graphical node of the given tree node.

        Args:
            treeNode (Node): The node to animate

        Returns:
            None: Nothing
        """

        self.__searchNode = self.__graphicalNodes.get(treeNode)

        # TODO: reset search node
