from PyQt6.QtCore import Qt, QLine
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFrame, QLabel

from .util import createVerticalLayout


class GraphicalNode(QWidget):
    """
    This class represents a graphical node in the tree and consists of 2*k keys and 2*k + 1 references.

    Args:
        order (int): The order of the tree.
        keys (list[int]): The keys of the node.
        parentReference (GraphicalNode): The parent reference this node is connected to.
    """

    def __init__(self, order, keys, parentReference):
        super().__init__()

        self.__parentReference = parentReference

        if keys:
            # Create a QHBoxLayout containing the references and keys in alternating order
            nodeLayout = QHBoxLayout()
            nodeLayout.setSpacing(0)

            # Start with a reference
            nodeLayout.addWidget(self.__createReference(), 1)

            for i in range(2*order):
                try:
                    key = self.__createKey(str(keys[i]))
                except IndexError:
                    key = self.__createKey("")

                nodeLayout.addWidget(key, 2)
                nodeLayout.addWidget(self.__createReference(), 1)

            self.setLayout(nodeLayout)

    @staticmethod
    def __createReference() -> QFrame:
        """
        This method creates a QFrame representing a reference in the tree. A reference is half the size of a key.

        Returns:
            QFrame: The reference box
        """

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.Panel)
        frame.setMinimumWidth(15)

        return frame

    @staticmethod
    def __createKey(key) -> QFrame:
        """
        This method creates a QFrame representing a key in the tree.
        Args:
            key (str): The value of the key

        Returns:
            QFrame: The key box
        """

        frame = QFrame()
        keyLabel = QLabel(str(key))
        keyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(createVerticalLayout([keyLabel]))
        frame.setFrameShape(QFrame.Shape.Panel)
        # Only show top and bottom border
        frame.setContentsMargins(0, 1, 0, 1)
        frame.setMinimumWidth(keyLabel.minimumWidth())

        return frame

    def getLine(self) -> QLine:
        """
        This method draws a line connecting this widget and the parent.

        Returns:
            QLine: The line which will connect this node to the reference
        """

        if self.__parentReference:
            parentGeometry = self.__parentReference.geometry()
            parentX = parentGeometry.x() + parentGeometry.width() // 2
            parentY = parentGeometry.y() + parentGeometry.height()

            selfX = self.geometry().x() + self.geometry().width() // 2
            selfY = self.geometry().y()

            return QLine(parentX, parentY, selfX, selfY)
        else:
            return QLine(0, 0, 0, 0)
