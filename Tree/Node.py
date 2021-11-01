class Node:
    """
    This class represents one node in the BalancedTree class

    Args:
        k(int): Order of the balanced tree, minimal number of keys in one node
        keys(list[int]): Keys of the node
        children(list[Node]): Children of the node, for n keys are n+1 children
        parent(Node or None): Parent of the node, if Parent is None, the node is the root
    """

    def __init__(self, k, keys=None, children=None, parent=None):
        self.k = k
        if keys is None:
            self.keys = []  # min k max 2k entries
        else:
            self.keys = keys
        if children is None:
            self.children = []  # max 2k + 1 children, references child nodes
        else:
            self.children = children
        if parent is None:
            self.parent = None
        else:
            self.parent = parent

    def hasKey(self, key):
        """
        Checks if the node contains a key.

        Args:
            key(int): The key that should be checked

        Returns:
            bool: True, if key is in node

        """

        return key in self.keys

    def addKeyAndChild(self, insert_key, child=None):
        """
        Inserts a key sorted into a leaf node (child=None)
        or insert a key and a corresponding child in a non leaf node (child=Node).

        Args:
            insert_key(int): Inserted key
            child(Node or None): Child, that should be inserted logically after insert_key

        Returns:

        """
        # insert new key into keys array so that it stays sorted
        key_insert_index = self.insert_key_sorted(insert_key)
        # insert new child into children array
        if child is not None:
            self.children.insert(key_insert_index + 1, child)

    def deleteKey(self, key) -> None:
        """
        Delete a key from the node, if the node is a leaf.

        Args:
            key(int):

        Returns:
            None

        """
        if self.isLeaf():
            self.keys.remove(key)
        else:
            raise ValueError("Cannot delete key, because node is not a leaf.")

    def replace_key(self,old_key,new_key) -> None:
        """

        Args:
            oldkey:
            newkey:

        Returns:
            None

        """

        self.keys = [new_key if key == old_key else key for key in self.keys]


    def split(self):
        """
        Splits a node, where an overflow occurred into three parts:
            1) The middle key
            2) The right_node, which contains keys+children on the right side of the middle key
            3) The left_node, which contains keys+children on the left side of the middle key

        The left node is the original node, but modified and the right node is a new node. And example is seen below:

            No overflow for k = 2

            keys:       [    1,   3,   6,   ,7    ]
            children:   [ R1   R2   R3   R4    R5 ]

            insert key 5 with child OR4 --> overflow (max keys are 2*K = 4)

            keys:       [    1,   3,     5,    6,   ,7     ]
            children:   [ R1   R2   R3     0R4    R5    R6 ]

            split into the following parts:

            keys:       [  1,   3,   ]      |5|     [     6,    ,7   ]
            children:   [R1   R2   R3]              [ 0R4    R5    R6]
            parts:        left_node    middle_index      right_node

        Returns:
            Tuple(Node,int,Node): Returns the middle element of the overfilled node, the right and left nodes:
                                 (left_node, middle_key, right_node)

        """
        if self.isOverflow():
            keys = self.keys
            # split list in two nodes, node one should contain the elements smaller than the middle elements,
            # node two should contain the elements bigger than the middle element.

            # split keys
            middle_index = len(keys) // 2  # floor division
            middle_key = keys[middle_index]
            keys_left_node = keys[:middle_index]
            keys_right_node = keys[middle_index + 1:]

            # split children
            children = self.children
            children_left_node = children[:int(len(children) // 2)]
            children_right_node = children[int(len(children) / 2):]

            # update current node (left_node)
            self.keys = keys_left_node
            self.children = children_left_node

            new_right_node = Node(self.k, keys=keys_right_node, children=children_right_node,
                                  parent=self.parent)

            # set new_right_node as the parent of it´s children
            for child in new_right_node.children:
                child.setParent(new_right_node)

            return self, middle_key, new_right_node

    def getSubtree(self, key_to_search):
        """
        Find the subtree, in which a key has to saved.

        Args:
            key_to_search(int): Key

        Returns:
            Node: child node, whose subtree contains the key_to_search

        """

        # iterate over the nodes keys until key_to_search is smaller than a key, to find the subtree that must contain
        # key_to_search
        for index, key in enumerate(self.keys):
            if key_to_search < key:
                # The index of "key" is equal to index of the child node that should be searched next.
                # This is seen in the example below for key_to_search = 2, where (key_to_search < key)
                # is first true for key=3 (node.keys[1]). Since the keys with values less than 3 and
                # greater than 2 lie by definition in the subtree referenced by R2, one should recursively
                # search this son. R2(node.children[1]) has the same index as the current key.
                # node.keys:               [1,   3,   7,   8]
                # correspondences:         /    /    /    /
                # node.children:         [R1,  R2,  R3,  R4,  R5]

                if self.isLeaf():
                    # a leaf has no children, key is not in the tree
                    return None
                else:
                    return self.children[index]

        # "key_to_search" is greater than all of the nodes keys
        # If the node isn´t a leaf, the key is in the subtree, where the last reference of node.children points to.
        if self.isLeaf():
            return None
        else:
            return self.children[-1]

    def isLeaf(self) -> bool:
        """
        Checks, if the node is a leaf (has no children)

        Returns:
            bool: True if node is a leaf

        """

        return self.children == []

    def isOverflow(self) -> bool:
        """
        Checks, if the node had an overflow. This happens, when the max number of key elements of (2*k) is exceeded.

        Returns:
            bool: True, if an overflow occurred

        """
        return len(self.keys) > 2 * self.k

    def isUnderflow(self) -> bool:
        """
        Checks, if the node had an underflow. This happens, when the node has less than the minimum number of key
        elements (k).

        Returns:
            bool: True, if an underflow occurred

        """
        return len(self.keys) < self.k

    def has_minimal_elements(self) -> bool:
        """
        checks, if the node has minimal number of elements.

        Returns:

        """
        return len(self.keys) == self.k

    def insert_key_sorted(self, insert_key) -> int:
        """
        Insert key into the correct position of the nodes sorted key array and return the index.

        Args:
            insert_key(int): Key to be inserted

        Returns:
            int: Index of new key

        """
        for index, key in enumerate(self.keys):
            if insert_key < key:
                self.keys.insert(index, insert_key)
                return index

        self.keys.append(insert_key)
        return len(self.keys) - 1

    def __str__(self) -> str:
        """
        Override the stringify method of Node, return in string representation.

        Returns:
            str: Node string

        """
        return f'[{" ".join(str(x) for x in self.keys)}]'

    # getters and setters

    def getParent(self):
        """

        Returns:
            Node: Parent of current node

        """
        return self.parent

    def setParent(self, parent):
        self.parent = parent

    def getChildren(self):
        return self.children

    def getKeys(self):
        return self.keys
