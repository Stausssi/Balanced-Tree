"""
tests, insert in empty tree
"""

from Tree.BalancedTree import BalancedTree

bt = BalancedTree(2)

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

print("---------32------------")

bt.insert(32)
print(bt)

print("---------Search 26------------")

print(bt.search(26))