from .Node import Node


class BalancedTree:
    """
    This class represents a balanced tree and handles operations (such as inserting, deleting or searching) on it

    Args:
        k (int): Order of the balanced tree, minimal number of keys in one node, max is 2*k
    """

    def __init__(self, k):
        self.root = Node(k)
        self.k = k

    def insert(self, insert_key) -> None:
        """
        Inserts a new key into the binary tree

        Args:
            insert_key(int): Key to be inserted

        Returns:
            None

        """
        # find the node to insert the new key
        target_node, found_key = self.search(insert_key)
        if found_key is not None:
            # key was found in tree
            raise ValueError(f"{found_key} is already in the tree.")
        else:
            # insert "key" into tree in node "target_node" recursively
            self.__recursive_insert(target_node, insert_key)

    def __recursive_insert(self, node, key, child=None) -> None:
        """
        Recursively inserts a key into a node. If the node is full, split the node into 2 and insert the middle key into
        the parent. If the parent is full and the root, create a new root.

        Args:
            node(Node): Node where the key should be inserted
            key(int): key that should be inserted
            child(Node): Reference to a child node, whose reference should be inserted after "key".
                    ATTENTION ! This should only be used for inserting references into non leaf nodes

        Returns:
            None

        """
        node.addKeyAndChild(key, child)

        if node.isOverflow():
            # split node into two nodes and middle key
            new_left_node, middle_key, new_right_node = node.split()
            # check if node is the root
            if node.getParent() is None:
                # node is the root
                # make new root with the middle_key and the left and right node as children
                new_root = Node(self.k, keys=[middle_key], children=[new_left_node, new_right_node], parent=None)
                # set new root as parent
                new_left_node.setParent(new_root)
                new_right_node.setParent(new_root)
                # set new root as tree root
                self.root = new_root
            else:
                # recursively insert middle_key into the parent node of the "node"
                # also add reference to the new_right_node after the middle_key in the parent node
                parent_node = new_left_node.getParent()
                self.__recursive_insert(parent_node, middle_key, child=new_right_node)

    def search(self, key):
        """
        Searches the whole balanced tree for a given key from the root recursively.

        Args:
            key(int): Key that is searched for in the balanced tree

        Returns:
            Tuple(Node,int): An Integer if the key was found, else None

        """
        # recursively search the tree for "key"
        return self.__recursive_search(self.root, key)

    def __recursive_search(self, node, key_to_search):
        """
        Searches the balanced tree from a node for a given key recursively.

        Args:
            node(Node): The Node that should be searched recursively
            key_to_search(int): Key to search for

        Returns:
            Tuple(Node,int): Either (Node, int): key was found and the node it was found in
                            or (Node, None): key was not found, should be inserted in node

        """

        if node.hasKey(key_to_search):
            # the key is returned, data could also be returned
            return node, key_to_search
        else:
            # determine next child node to search recursively
            child_node = node.getSubtree(key_to_search)
            if child_node is None:
                # key could not be found, should be inserted at node
                return node, None
            else:
                return self.__recursive_search(child_node, key_to_search)

    def isEmpty(self) -> bool:
        """
        Returns whether the tree is empty.

        Returns:
            bool: True, if the tree is empty, false otherwise
        """

        return self.root.isLeaf() and len(self.root.keys) == 0

    def getAllValues(self) -> list[int]:
        """
        Returns all values kept in the tree.

        Returns:
            list[int]: A list of integers representing the values of the tree.
        """

        values = []
        nodes = [self.root]

        # As long as there are nodes in the list
        while nodes:
            for node in nodes:
                # Remove this node from the list
                nodes.remove(node)

                # Add all children of the node to list
                nodes.extend(node.children)

                # Add the keys of the node to the value list
                values.extend(node.keys)

        return values

    def __str__(self):
        out = []
        # Basic list contains the root only
        nodes: list[list[Node]] = [[self.root]]
        layer = 1

        # Construct the layout
        while len(nodes) > 0:

            out.append("")
            current_string = len(out) - 1

            # Create a new layer
            nodes.append([])
            for node in nodes[0]:
                # Create a label containing the keys of the node
                out[current_string] += str(node)

                if not node.isLeaf():
                    # Add the children of the node to the next layer
                    nodes[1].extend(node.children)

            # Remove the old layer
            nodes = nodes[1:]

            # Remove empty layers
            for _ in range(nodes.count([])):
                nodes.remove([])

            layer += 1

        # center all strings in the array based on the length of the last one
        last_string_length = len(out[-1])
        out_string = ""
        for row in out:
            out_string = out_string + "\n" + row.center(last_string_length)

        return out_string
