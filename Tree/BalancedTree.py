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
        Searches the balanced tree for a given key

        Args:
            key(int): Key that is searched for in the balanced tree

        Returns:

        """
        # recursively search the tree for "key"
        return self.__recursive_search(self.root, key)

    def __recursive_search(self, node, key_to_search):
        """
        Recursively searches for the key in the given node

        Args:
            node:
            key_to_search:

        Returns:

        """

        # todo: edge case: Key List not full    [1,   2,   None,None]
        # todo:                       nodes:[R1,   R2,  R3, None, None
        # if key is none, search R3 (is None ? --> kann nicht sein, weil immer n+1 sons)

        # iterate over node.keys, until key_to_search is no longer smaller than the key
        for key in node.keys:
            if key == key_to_search:
                # found key
                return key
            elif key_to_search < key:
                # The index of "key" is equal to index of the child node that should be searched next.
                # This is seen in the example below for key_to_search = 2, where (key_to_search < key)
                # is first true for key=3 (node.keys[1]). Since the keys with values less than 3 and
                # greater than 2 lie by definition in the subtree referenced by R2, one should recursively
                # search this son. R2(node.sons[1]) has the same index as the current key.

                # node.keys:            [1,   3,   7,   8]
                # correspondences:      /    /    /    /
                # node.sons:         [R1,  R2,  R3,  R4,  R5]

                child_index = node.keys.index(key)

                # recursively search the child node and return it´s key
                return self.__recursive_search(node.keys[child_index], key_to_search)
        else:
            # This get´s executed, then the for-loop completes, this only happens, if "key_to_search" is greater
            # than all of the nodes keys.
            # This can happen in the following cases:
            # 1) The key is in the subtree, where the last reference of node.sons points to.
            #    If "key_to_search" is 9 for example, this would indicate,
            #    that the key is in R5 since 9 is greater than 8.
            #         node.keys:      [1,   3,   7,   8]
            # correspondences:        /    /    /    /
            #         node.sons:   [R1,  R2,  R3,  R4,  R5]
            # 2) The reference to the last son is "None", which means that "key_to_search" is not in the tree

            last_node = node.sons[::-1]
            if last_node is None:
                # returning None indicates, no key was found in the tree
                return None
            else:
                # recursively search the last node
                return self.__recursive_search(last_node, key_to_search)


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
        self.keys = [None] * (2 * k)  # every node with k sons should save max k-1 keys
        self.sons = [None] * (2 * k + 1)  # max k sons, references child nodes

    def addKeys(self):
        """

        Returns:

        """
        pass

    def isLeaf(self):
        """

        Returns:

        """
        return self.sons == [None] * (2 * self.k + 1)
