from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)

keys = [1, 22, 21, 12, 3, 11, 7, 123, 88]

for key in keys:
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt)
