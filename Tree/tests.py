"""
tests
"""

from Tree.BalancedTree import BalancedTree
from Tree.Node import Node


node1 = Node(2, keys=[1, 2, ])
node2 = Node(2, keys=[4, 5])
node3 = Node(2, keys=[8, 9])
root = Node(2, keys=[3, 7], children=[node1, node2, node3])
node1.setParent(root)
node2.setParent(root)
node3.setParent(root)

bt = BalancedTree(2)
bt.root = root

print(bt)

print("---------10-----------")

bt.insert(10)
print(bt)

print("---------14------------")

bt.insert(14)
print(bt)

print("---------20------------")

bt.insert(20)
print(bt)

print("---------21------------")

bt.insert(21)
print(bt)

print("---------24------------")

bt.insert(24)
print(bt)

print("---------26------------")

bt.insert(26)
print(bt)

print("---------28------------")

bt.insert(28)
print(bt)

print("---------30------------")

bt.insert(30)
print(bt)

print("---------32------------  --> Root split")

bt.insert(32)
print(bt)
