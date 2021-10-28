class Node:
    """
    This class represents one node in the BalancedTree class

    Args:
        k(int): Order of the balanced tree, minimal number of keys in one node
        isRoot(bool): Determines if Node is the leaf
    """

    def __init__(self, k, isRoot=False, keys=None, children=None):
        self.k = k
        self.isRoot = isRoot
        self.keys = [None] * (2 * k)  # min k max 2k entries
        if keys is not None:
            for key in keys:
                self.addKeyAndChild(key, None)
        self.sons = [None] * (2 * k + 1)  # max 2k + 1 sons, references child nodes
        self.parent = None
        self.overflow = []

    def hasKey(self, key):
        """
        Checks if a node contains a key

        Args:
            key(int): The key that should be checked

        Returns:
            bool: True, if key is in node

        """

        return key in self.keys

    def addKeyAndChild(self, key, child):
        """
        Adds a key to a node

        Args:
            key:
            child:

        Returns:

        """
        if len(self.keys) < (2 * self.k):
            # get index of first None value
            first_none_index = next(self.keys.index(key) for key in self.keys if key is None)
            # insert new key into keys array
            self.keys[first_none_index] = key
            # insert new child into sons array
            self.sons[first_none_index + 1] = child
        else:
            self.overflow = [key, child]
            raise ValueError("Node is full")

    def fixOverflowAndSplit(self):
        """
        orders entries, split node correctly and returns a new node
        use for leaf and tree overflows, also change links in non leaf nodes

        # Todo: Does not split the references to child objects

        Returns:
            Tuple(int,Node): Returns the middle element of the overfilled node and an new node with the successors of
                            of the middle node

        """
        if self.overflow:
            keys = self.keys
            # find index after which the new key has to be inserted
            key_insert_index = next([self.keys.index(key) for key in self.keys if self.overflow < key])
            keys.insert(key_insert_index, self.getOverflow()[0])

            # split list in two nodes, node one should contain the elements smaller than the middle elements,
            # node two should contain the elements bigger than the middle element.
            # It should be accounted for k, the minimal number of nodes.
            # Since keys have at least k and at most 2k entries, if an overflow occurs, keys will always have 2k+1
            # entries, which is always odd. The list is split like so:
            # k=3 + Overflow: [1,3,5 |7| 9,10,11] --> split list at |
            # k=2 + Overflow: [1,3 |5| 6,7] --> split list at |
            # [    1,   3,   |5|,    6,   ,7   ]
            #   R1   R2   R3     oR4    R5    R6

            # keys
            middle_index = int(len(keys) / 2)  # always works for odd list length
            middle_key = keys[middle_index]
            left_key_sublist = keys[:middle_index]
            right_key_sublist = keys[middle_index + 1:]

            # children

            # [    1,   3,   6,   ,7    ]
            # [ R1   R2   R3   R4    R5 ]

            # insert key 5 with OR4

            # [    1,   3,   |5|,    6,   ,7   ]
            #   R1   R2   R3     0R4    R5    R6

            # [    1,   3,   |5|,    6,   ,7   ]
            #   R1   R2   R3     0R4    R5    R6

            # [    1,   3,  ]     |5|    [    6,   ,7   ]
            #   R1   R2   R3              0R4    R5    R6

            # insert the "Overflow-Node" at key_insert_index + 1

            sons = self.sons
            sons.insert(key_insert_index + 1, self.getOverflow()[1])
            left_sons_sublist = sons[:len(sons)/2 - 1]  # length of sons with overflow is always even
            right_sons_sublist = sons[len(sons)/2:]

            # update current node with keys before the middle key
            self.keys = left_key_sublist
            self.sons = left_sons_sublist
            # reset Overflow
            self.setOverflow([])

            # todo: Split Children
            return middle_key, Node(self.k, keys=right_sublist)

    def getSubtree(self, key_to_search):
        """

        Args:
            key_to_search(int): Key

        Returns:
            Node: child node, whose subtree contains the key_to_search

        """

        for index, key in enumerate(self.keys):
            if key is None or key_to_search < key:
                # The index of "key" is equal to index of the child node that should be searched next.
                # This is seen in the example below for key_to_search = 2, where (key_to_search < key)
                # is first true for key=3 (node.keys[1]). Since the keys with values less than 3 and
                # greater than 2 lie by definition in the subtree referenced by R2, one should recursively
                # search this son. R2(node.sons[1]) has the same index as the current key.
                # node.keys:            [1,   3,   7,   8]
                # correspondences:      /    /    /    /
                # node.sons:         [R1,  R2,  R3,  R4,  R5]

                # When not all keys are occupied, and key_to_search is greater than all keys, the loop needs to stop
                # at the first None occurrence and pick the child node at that index as seen below
                # node.keys:            [1,   3,  None, None]
                # correspondences:      /    /    /    /
                # node.sons:         [R1,  R2,  R3,  R4,  R5] --> R3 would need to be picked

                # return child node, can be None
                return self.sons[index]

        # This get´s executed, when the for-loop completes, this only happens, if "key_to_search" is greater
        # than all of the nodes keys. The key is in the subtree, where the last reference of node.sons points to.

        return self.sons[-1]

    def isLeaf(self):
        """
        Checks, if the node is a leaf (has no children)

        Returns:
            bool: True if node is a leaf

        """

        return self.sons == [None] * (2 * self.k + 1)

    # getters and setters

    def getOverflow(self):
        return self.overflow

    def setOverflow(self, overflow):
        self.overflow = overflow

    def getParent(self):
        return self.parent

    def setParent(self, parent):
        self.parent = parent
