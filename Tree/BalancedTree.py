from .Node import Node


class BalancedTree:
    """
    This class represents a balanced tree and handles operations (such as inserting or deleting) on it

    Args:
        k (int): Order of the balanced tree, minimal number of keys in one node, max is 2*k
    """

    def __init__(self, k):
        self.root = Node(k, isRoot=True)

    def insert(self, insert_key):
        """
        insert a new key into the binary tree

        Args:
            insert_key(int):

        Returns:

        """
        # find the node to insert the new key
        target_node, found_key = self.search(insert_key)
        if found_key is not None:
            # key was found in tree
            raise ValueError(f"{found_key} is already in the tree.")
        else:
            # insert "key" into tree in node "target_node"
            self.__recursive_insert(target_node, insert_key)

    def __recursive_insert(self, target_node, key, child=None):
        """
        Recursively inserts a key into a node, if the node is full, split the node and insert the middle key into
        the parent.

        Args:
            target_node(Node): Node where the key should be inserted
            key(int): key that should be inserted
            child(Node): Reference to a child node, whose reference should be inserted after "key".
                    This should only be used for inserting keys into non leaf nodes

        Returns:
            None

        """
        try:
            target_node.addKeyAndChild(key, child)
        except ValueError:
            # split node into two nodes
            middle_key, new_node = target_node.fixOverflowAndSplit()
            parent_node = target_node.getParent()

            # recursively insert middle_key into the parent node of the target_node
            # also add reference to the new node after the middle_key in the parent node
            # todo: Root ?
            self.__recursive_insert(parent_node, middle_key, child=new_node)

    def search(self, key):
        """
        Searches the balanced tree for a given key from the root

        Args:
            key(int): Key that is searched for in the balanced tree

        Returns:
            Tuple(Node,int): An Integer if the key was found, else None

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
            Tuple(Node,int): Either (Node, int): key was found and the node it was found in
                            or (Node, None): key was not found, should be inserted in node

        """

        if node.hasKey(key_to_search):
            # the key is returned, data could also be returned
            return node, key_to_search
        else:
            # determine child node to search recursively
            child_node = node.getSubtree(key_to_search)
            if child_node is None:
                # key could not be found, should be inserted at node
                return node, None
            else:
                return self.__recursive_search(child_node, key_to_search)
