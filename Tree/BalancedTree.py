from __future__ import annotations

from typing import Tuple

from loguru import logger

import config
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

        self.__searchCount = 0

    def search(self, key) -> Tuple[Node, int, int]:
        """
        Searches the whole balanced tree for a given key from the root recursively.

        Args:
            key (int): Key that is searched for in the balanced tree

        Returns:
            Tuple[Node,int]: The node the key was found in and the key

        """

        self.__searchCount = 0

        # recursively search the tree for "key"A
        return self.__recursive_search(self.root, key)

    def __recursive_search(self, node, key_to_search) -> tuple[Node, int, int] | tuple[Node, None, int]:
        """
        Searches the balanced tree from a node for a given key recursively.

        Args:
            node (Node): The Node that should be searched recursively
            key_to_search (int): Key to search for

        Returns:
            Tuple[Node,int]: Either (Node, int): key was found and the node it was found in
                            or (Node, None): key was not found, should be inserted in node

        """
        # logging
        logger.info(f"SEARCH FOR KEY {key_to_search} in node: {node}")

        # send the current node to the GUI, to visualize searching
        if not config.DEBUG:
            config.mainWindow.addNoteToPath(node)

        self.__searchCount += 1

        if node.hasKey(key_to_search):
            # key was found
            # the key is returned, data could also be returned
            logger.info(f"KEY {key_to_search} WAS FOUND IN NODE: {node}")
            return node, key_to_search, self.__searchCount
        else:
            # determine next child node to search recursively
            child_node = node.getSubtree(key_to_search)
            if child_node is None:
                # key could not be found, should be inserted at node
                logger.info(f"KEY COULD NOT BE FOUND, SHOULD BE INSERTED IN NODE: {node}")
                return node, None, self.__searchCount
            else:
                return self.__recursive_search(child_node, key_to_search)

    def insert(self, insert_key) -> None:
        """
        Inserts a new key into the binary tree

        Args:
            insert_key (int): Key to be inserted

        Returns:
            None

        """

        # find the node to insert the new key
        target_node, found_key, _ = self.search(insert_key)
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
            node (Node): Node where the key should be inserted
            key (int): key that should be inserted
            child (Node): Reference to a child node, whose reference should be inserted after "key".
                    ATTENTION ! This should only be used for inserting references into non leaf nodes

        Returns:
            None

        """
        logger.info(f"INSERT KEY {key} WITH CHILD {child} INTO NODE {node}")

        # insert key and child into node at correct position.
        node.addKeyAndChild(key, child)

        if node.isOverflow():
            # split node into two nodes and middle key
            new_left_node, middle_key, new_right_node = node.split()

            # logging
            logger.info(f"OVERFLOW, SPLIT NODE INTO LEFT NODE:{new_left_node}, MIDDLE_KEY:{middle_key}"
                        f" AND RIGHT NODE:{new_right_node}")

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

                # logging
                logger.info(f"MAKE NEW ROOT {new_root} WITH LEFT AND RIGHT NODE AS CHILDREN")
            else:
                # recursively insert middle_key into the parent node of the "node"
                # also add reference to the new_right_node after the middle_key in the parent node
                parent_node = new_left_node.getParent()
                self.__recursive_insert(parent_node, middle_key, child=new_right_node)

    def delete(self, key) -> None:
        """
        Delete a key from the balanced tree. This is an implementation of the following description
        (https://www.cs.rhodes.edu/~kirlinp/courses/db/f16/handouts/btrees-deletion.pdf):

        Deletion has two base cases:

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


        Args:
            key(int): key to delete from balanced tree

        Returns:
            None: Nothing

        """

        # find the node to delete the key
        target_node, found_key, _ = self.search(key)
        if found_key is not None:

            # check if target_node is leaf node
            if target_node.isLeaf():
                # logging
                logger.info(f"DELETE KEY FROM LEAF NODE: {target_node}")

                # delete from leaf and rebalance the tree, if an underflow occurred
                target_node.deleteKey(found_key)

                # only rebalance the node in an underflow, if it is not a leaf and the root at the same time
                if target_node.isUnderflow() and not (target_node.isLeaf() and target_node.isRoot()):
                    # logging
                    logger.info(f"LEAF NODE UNDERFLOW: {target_node}")

                    self.__recursive_rebalance(target_node)
            else:
                # target_node is an internal node

                # get inorder predecessor and check if node has keys to spare
                replacement_node, replacement_key = self.__get_in_order_predecessor(target_node, key)
                if not replacement_node.more_than_minimal_elements():
                    # use in order successor instead
                    replacement_node, replacement_key = self.__get_in_order_successor(target_node, key)

                    # logging
                    logger.info(
                        f"REPLACE KEY {key} WITH IN ORDER SUCCESSOR {replacement_key} FROM NODE {replacement_node}"
                    )
                else:
                    # logging
                    logger.info(
                        f"REPLACE KEY {key} WITH IN ORDER PREDECESSOR {replacement_key} FROM NODE {replacement_node}"
                    )

                # replace element that should be deleted with the predecessor_key
                target_node.replace_key(key, replacement_key)

                # delete key from replacement node
                replacement_node.deleteKey(replacement_key)

                # recursively fix predecessor node if it had an underflow
                if replacement_node.isUnderflow():
                    self.__recursive_rebalance(replacement_node)
        else:
            # key wasn't found in tree
            raise ValueError(f"{key} is not in the tree.")

    def __recursive_rebalance(self, deficient_node) -> None:
        """
        Recursively rebalance the tree upwards from the given node to maintain the balanced tree properties.

        The following description is from:
        (https://www.cs.rhodes.edu/~kirlinp/courses/db/f16/handouts/btrees-deletion.pdf):

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

        • If the parent is the root and now has no elements, then free it and make the merged node the
            new root (tree becomes shallower)

        • Otherwise, if the parent has fewer than the required number of elements, then rebalance the parent

        Args:
            deficient_node(Node): The node, that has less than k keys and should be rebalanced.

        Returns:
            None: Nothing

        """

        logger.info(f"NODE {deficient_node} IS DEFICIENT, START REBALANCING")

        # check if either left or right sibling exist and have more than k elements
        # if so, rotate left/right, and else merge the deficient node with either the left or right sibling
        right_sibling, seperator_key_index_right = deficient_node.get_right_sibling()
        left_sibling, seperator_key_index_left = deficient_node.get_left_sibling()
        parent = deficient_node.getParent()

        if right_sibling is not None and right_sibling.more_than_minimal_elements():
            # rotate left
            logger.info(f"ROTATE LEFT: DEF{deficient_node},PARENT{parent},RIGHT SIBLING{right_sibling}")
            self.__rotate_left(deficient_node, right_sibling, seperator_key_index_right)
            logger.info(f"AFTER ROTATION: DEF{deficient_node},PARENT{parent},RIGHT SIBLING{right_sibling}")
        elif left_sibling is not None and left_sibling.more_than_minimal_elements():
            # rotate right
            logger.info(f"ROTATE RIGHT: LEFT SIBLING{left_sibling},PARENT{parent},DEF{deficient_node}")
            self.__rotate_right(deficient_node, left_sibling, seperator_key_index_left)
            logger.info(f"AFTER ROTATION: LEFT SIBLING{left_sibling},PARENT{parent},DEF{deficient_node}")
        else:
            # if right sibling exist, merge with right sibling, else merge with left sibling

            if right_sibling is not None:
                # merge deficient node with right sibling
                logger.info(
                    f"MERGE DEFICIENT NODE WITH RIGHT SIBLING: DEF{deficient_node}, RIGHT SIBLING{right_sibling}")
                merged_node = self.__merge_nodes(deficient_node, right_sibling, seperator_key_index_right)
                logger.info(f"MERGED NODE: {merged_node}")
            else:
                # merge deficient node with left sibling
                logger.info(f"MERGE DEFICIENT NODE WITH LEFT SIBLING: LEFT SIBLING{left_sibling}, DEF{deficient_node}")
                merged_node = self.__merge_nodes(left_sibling, deficient_node, seperator_key_index_left)
                logger.info(f"MERGED NODE: {merged_node}")

            # parent has now one element less than before.
            # if parent is the root and now has no elements, make the merged node the new root
            if parent.isRoot() and parent.getKeys() == []:
                self.root = merged_node
                merged_node.setParent(None)

                # logging
                logger.info(f"PARENT NODE IS ROOT AND EMPTY, NEW ROOT: {merged_node}")
            elif parent.isUnderflow():
                # if parent had an underflow, recursively rebalance the parent if it is not the root
                if not parent.isRoot():
                    self.__recursive_rebalance(parent)

    def __merge_nodes(self, left_node, right_node, separator_index) -> Node:
        """
        Merge two nodes that have the minimum number of elements, lie next to each other and have the same
        parent into one node.

        This is done by combining the children/keys of left and right node, together with their seperator of the parent.
        This is seen in the example below (k = 1):

                                         seperator
                                             |
               [ 5    8 ]     delete 1     [ 5    8 ]   merge [] and [6]        [ 8 ]
             [1]  [6]  [9]   -------->   [x]  [6]  [9]  ---------------->    [5 6] [9 ]


        This is done using the following steps:

        1. Copy the separator to the end of the left node (the left node may be the deficient node, or it may be
            the sibling with the minimum number of elements)
        2. Move all elements from the right node to the left node (the left node now has the maximum number
            of elements, and the right node – empty)
        3. Remove the separator from the parent along with its empty right child (the parent loses an element)

        Args:
            left_node (Node): Node on the left
            right_node (Node): Node on the right
            separator_index (int): Index of key in parent, that logically separates left_node and right_node

        Returns:
            Node: The merged node

        """

        # add seperator key in parent to the left node
        parent = left_node.getParent()
        seperator = parent.getKeys()[separator_index]
        left_node.addKeyAndChild(seperator)

        # create new node from the left and right nodes keys/children
        keys = left_node.getKeys()
        keys.extend(right_node.getKeys())
        children = left_node.getChildren()
        children.extend(right_node.getChildren())
        merged_node = Node(self.k, keys=keys, children=children, parent=parent)

        # reset parent of new nodes children to the merged_node
        for child in children:
            child.setParent(merged_node)

        # remove seperator from parent
        parent.deleteKey(seperator)
        # remove child after seperator in parent and replace reference to child before seperator with new node
        parent.deleteChild(right_node)
        parent.setChild(merged_node, separator_index)

        return merged_node

    @staticmethod
    def __rotate_left(deficient_node, right_sibling, seperator_index) -> None:
        """
        Rotate an element from right_sibling to parent and from parent to deficient_node, so that deficient node has
        k elements. When deficient_node and right_sibling are internal nodes, also transfer the first child of
        right_sibling to the deficient_node.

        Args:
            deficient_node (Node): The Node that receives a key during the rotation
            right_sibling (Node): The node that gives a key, must have more than k elements and is on the right of
                                    deficient_node
            seperator_index (int): The index of the key, that logically separates deficient_node and right_sibling

        Returns:
            None: Nothing

        """

        parent = deficient_node.getParent()

        # insert seperator at the end of deficient node
        seperator_key = parent.getKeys()[seperator_index]
        deficient_node.insert_key(-1, seperator_key)

        # insert first child of right_sibling at the end of deficient node if nodes are internal nodes
        if not right_sibling.isLeaf():
            first_child_right_sibling = right_sibling.popChild(0)
            deficient_node.insert_child(-1, first_child_right_sibling)
            # set parent to deficient node
            first_child_right_sibling.setParent(deficient_node)

        # Replace the separator in the parent with the first element of the right sibling
        # and delete first key from right sibling
        first_key_right_sibling = right_sibling.popKey(0)
        parent.replace_key(seperator_key, first_key_right_sibling)

    @staticmethod
    def __rotate_right(deficient_node, left_sibling, seperator_index) -> None:
        """
        Rotate an element from left_sibling to parent and from parent to deficient_node, so that deficient node has
        k elements. When deficient_node and right_sibling are internal nodes, also transfer the last child of
        left_sibling to the deficient_node.

        Args:
            deficient_node (Node): The Node that receives a key during the rotation
            left_sibling (Node): The node that gives a key, must have more than k elements and is on the left of
                                    deficient_node
            seperator_index (int): The index of the key, that logically separates deficient_node and right_sibling

        Returns:
            None: Nothing

        """

        parent = deficient_node.getParent()

        # insert seperator at the start of deficient node
        seperator_key = parent.getKeys()[seperator_index]
        deficient_node.insert_key(0, seperator_key)

        # insert last child of left_sibling at the start of deficient node if nodes are internal nodes
        if not left_sibling.isLeaf():
            # get last child of left sibling
            last_child_left_sibling = left_sibling.popChild(-1)
            # set parent to deficient node
            last_child_left_sibling.setParent(deficient_node)
            # insert at the start of deficient node
            deficient_node.insert_child(0, last_child_left_sibling)

        # Replace the separator in the parent with the last element of the left sibling
        # and delete last element from left sibling
        last_key_left_sibling = left_sibling.popKey(-1)
        parent.replace_key(seperator_key, last_key_left_sibling)

    @staticmethod
    def __get_in_order_predecessor(node, key) -> Tuple[Node, int]:
        """
        Get the largest key in the subtree of the child that is on the left of the key in the node.
        Return the largest key and the node it is in.

        Args:
            node (Node): The node where "key" is in
            key (int): The key, whose in order predecessor should be found.

        Returns:
            Tuple[Node, int]: The largest key and the node it is in.

        """

        if not node.hasKey(key):
            raise ValueError(f"Node does not contain {key}")
        elif node.isLeaf():
            raise ValueError("Node is a leaf and does not have a in order predecessor")
        else:
            # get reference to child on the left of "key" --> index equal to key as seen below
            # node.keys:                [1,   3,   7,   8]
            # correspondences:          /    /    /    /
            # node.children:          [R1,  R2,  R3,  R4,  R5]
            #                                     ^
            # current key(7)--> left child of key |

            left_child = node.getChildren()[node.getKeys().index(key)]

            traversing_node = left_child

            # traverse the tree with the first reference of the node until a leaf is reached
            while not traversing_node.isLeaf():
                traversing_node = traversing_node.getChildren()[-1]

            largest_key = traversing_node.getKeys()[-1]

            # return the biggest key in the leaf node
            return traversing_node, largest_key

    @staticmethod
    def __get_in_order_successor(node, key) -> Tuple[Node, int]:
        """
        Get the smallest key in the subtree of the right child of the given node and key. Return the key and the node
        it is in.

        Args:
            node (Node): The node where "key" is in
            key (int): The key, whose in order successor should be found.

        Returns:
            Tuple[Node, int]: The largest key and the node it is in.

        """

        if not node.hasKey(key):
            raise ValueError(f"Node does not contain {key}")
        elif node.isLeaf():
            raise ValueError("Node is a leaf and does not have a in order successor")
        else:
            # get reference to child on the right of "key" --> index equal to index of key + 1 as seen below:
            # node.keys:               [1,   3,   7,   8]
            # correspondences:         /    /    /    /
            # node.children:         [R1,  R2,  R3,  R4,  R5]
            #                                         ^
            #                      current key (7)    | right child of key

            right_child = node.getChildren()[node.getKeys().index(key) + 1]

            traversing_node = right_child

            # traverse the tree with the first children of a node until a leaf is reached --> first is smallest element
            while not traversing_node.isLeaf():
                traversing_node = traversing_node.getChildren()[0]

            smallest_key = traversing_node.getKeys()[0]

            # return the smallest key in the leaf node
            return traversing_node, smallest_key

    def isEmpty(self) -> bool:
        """
        Returns whether the tree is empty.

        Returns:
            bool: True, if the tree is empty, false otherwise
        """

        return self.root.isLeaf() and len(self.root.keys) == 0

    def getAllValues(self) -> set[int]:
        """
        Returns all values kept in the tree.

        Returns:
            set[int]: A set of integers representing the values of the tree.
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

        return set(values)

    def __str__(self) -> str:
        """
        Overrides the string representation of the tree, return a formatted tree.

        Returns:
            str: Formatted Tree

        """

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
