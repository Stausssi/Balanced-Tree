class BalancedTree:
    """
    This class represents a balanced tree and handles operations (such as inserting or deleting) on it

    Args:
        k (int): Order of the balanced tree, minimal number of keys in one node
    """

    def __init__(self, k):
        self.root = Node(k, isRoot=True)

    def insert(self, key):
        """
        insert a new

        Args:
            key:

        Returns:

        """
        pass

    def search(self, key):
        """
        Searches the balanced tree for a given key from the root

        Args:
            key(int): Key that is searched for in the balanced tree

        Returns:
            int: An Integer if the key was found, else None

        """
        # recursively search the tree for "key"
        return self.__recursive_search(self.root, key)

    def __recursive_search(self, node, key_to_search):
        """
        Recursively searches for the key in the given node

        Args:
            node(Node): The Node that should be searched recursively
            key_to_search(int): Key

        Returns:
            Tuple(Node,int): An Integer if the key was found, else None

        """

        if node.hasKey(key_to_search):
            # the key is returned, data could also be returned
            return self, key_to_search
        else:
            # determine child node to search recursively
            child_node = node.getSubtree(key_to_search)
            if child_node is None:
                return None, None
            else:
                return self.__recursive_search(child_node, key_to_search)


class Node:
    """
    This class represents one node in the BalancedTree class

    Args:
        k(int): Order of the balanced tree, minimal number of keys in one node
        isRoot(bool): Determines if Node is the leaf
    """

    def __init__(self, k, isRoot=False):
        self.k = k
        self.isRoot = isRoot
        self.keys = [None] * (2 * k)  # min k max 2k entries
        self.sons = [None] * (2 * k + 1)  # max 2k + 1 sons, references child nodes

    def hasKey(self, key):
        """
        Checks if a node contains a key

        Args:
            key(int): The key that should be checked

        Returns:
            bool: True, if key is in node

        """

        return key in self.keys

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
