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
            Tuple[Node,int]: An Integer if the key was found, else None

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

    def delete(self, key) -> None:
        """
        Delete a key from the balanced tree. This is an implementation of the following algorithm
        (https://www.cs.rhodes.edu/~kirlinp/courses/db/f16/handouts/btrees-deletion.pdf):

        Deletion from a leaf node
            1. Search for the value to delete.
            2. If the value is in a leaf node, simply delete it from the node.
            3. If underflow happens, rebalance the tree as described in section "Rebalancing after deletion" below.

        Deletion from an internal node
            1. Choose a new separator (the largest element in the left subtree), remove it from the leaf node it is in,
            and replace the element to be deleted with the new separator.
            2. The previous step deleted an element (the new separator) from a leaf node. If that leaf node is now
            deficient (has fewer than the required number of nodes), then rebalance the tree starting from the leaf
            node.

        Rebalancing after deletion
        Rebalancing starts from a leaf and proceeds toward the root until the tree is balanced. If deleting an element
        from a node has brought it under the minimum size, then some elements must be redistributed to bring all
        nodes up to the minimum. Usually, the redistribution involves moving an element from a sibling node that has
        more than the minimum number of nodes. That redistribution operation is called a rotation. If no sibling can
        spare a node, then the deficient node must be merged with a sibling. The merge causes the parent to lose a
        separator element, so the parent may become deficient and need rebalancing. The merging and rebalancing
        may continue all the way to the root. Since the minimum element count doesn't apply to the root, making the
        root be the only deficient node is not a problem. The algorithm to rebalance the tree is as follows:

        • If the deficient node's right sibling exists and has more than the minimum number of elements, then rotate
        left
            1. Copy the separator from the parent to the end of the deficient node (the separator moves down; the
            deficient node now has the minimum number of elements)
            2. Replace the separator in the parent with the first element of the right sibling (right sibling loses one
            node but still has at least the minimum number of elements)
            3. The tree is now balanced

        • Otherwise, if the deficient node's left sibling exists and has more than the minimum number of elements,
        then rotate right
            1. Copy the separator from the parent to the start of the deficient node (the separator moves down;
            deficient node now has the minimum number of elements)
            2. Replace the separator in the parent with the last element of the left sibling (left sibling loses one
            node but still has at least the minimum number of elements)
            3. The tree is now balanced

        • Otherwise, if both immediate siblings have only the minimum number of elements, then merge with a
        sibling sandwiching their separator taken off from their parent
            1. Copy the separator to the end of the left node (the left node may be the deficient node or it may be
            the sibling with the minimum number of elements)
            2. Move all elements from the right node to the left node (the left node now has the maximum number
            of elements, and the right node – empty)
            3. Remove the separator from the parent along with its empty right child (the parent loses an element)

        • If the parent is the root and now has no elements, then free it and make the merged node the
        new root (tree becomes shallower)
        • Otherwise, if the parent has fewer than the required number of elements, then rebalance the
        parent

        Args:
            key(int): key to delete

        Returns:
            None

        """

        # find the node to delete the key
        target_node, found_key = self.search(key)
        if found_key is not None:
            # check if target_node is leaf node
            if target_node.isLeaf():
                # delete from leaf and rebalance the tree, if an underflow occurred
                target_node.deleteKey()
                if target_node.isUnderflow():
                    self.__recursive_rebalance(target_node)
            else:
                # target_node is an internal node

                # pop largest element in left subtree of target_node
                predecessor_node, predecessor_key = self.__get_in_order_predecessor(target_node, key)
                # replace element that should be deleted with the predecessor_key
                target_node.replace_key(key, predecessor_key)

                # fix predecessor node if it had an underflow
                if predecessor_node.isUnderflow():
                    self.__recursive_rebalance(predecessor_node)
        else:
            # key wasn´t found in tree
            raise ValueError(f"{found_key} is not in the tree.")

    def __recursive_rebalance(self, node):
        """
        Recursively rebalance the tree upwards from the given node

        Args:
            node:

        Returns:

        """

    def __get_in_order_predecessor(self, node, key):
        """
        Get the largest key in the subtree of the left child of the given node and key. Return the key and the node
        it is in.

        Args:
            node:
            key:

        Returns:

        """

        if not node.hasKey(key):
            return ValueError(f"Node does not contain {key}")
        elif node.isLeaf():
            return ValueError("Node is a leaf and does not have a in order predecessor")
        else:
            left_child = node.getChildren()[node.getKeys().index(key) + 1]

            traversing_node = left_child

            # traverse the tree with the last children of the node until a leaf is reached
            while not traversing_node.isLeaf():
                traversing_node = traversing_node.getChildren()[-1]

            largest_key = traversing_node.getKeys()[-1]
            traversing_node.deleteKey(largest_key)

            # return the biggest key in the leaf node
            return traversing_node,largest_key

    def __get_in_order_successor(self, node, key):
        """
        Get the smallest key in the subtree of the right child of the given node and key. Return the key and the node
        it is in.

        Args:
            node:
            key:

        Returns:

        """

        if not node.hasKey(key):
            return ValueError(f"Node does not contain {key}")
        elif node.isLeaf():
            return ValueError("Node is a leaf and does not have a in order successor")
        else:
            right_child = node.getChildren()[node.getKeys().index(key)]

            traversing_node = right_child

            # traverse the tree with the first children of a node until a leaf is reached
            while not traversing_node.isLeaf():
                traversing_node = traversing_node.getChildren()[0]

            # return the smallest key in the leaf node
            return traversing_node, traversing_node.getKeys()[0]

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
