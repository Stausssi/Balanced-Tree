from Tree.BalancedTree import BalancedTree

bt = BalancedTree(2)

for key in range(10, 30):
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt)

bt.delete(22)

bt.delete(23)
