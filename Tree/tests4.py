from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)

keys = [1, 22, 21, 12, 3, 11, 7, 123]

for key in keys:
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt)


bt.insert(88)
print(bt)
