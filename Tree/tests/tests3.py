from Tree.BalancedTree import BalancedTree

bt = BalancedTree(2)

for i in range(60):
    print(f"---------- {i} ----------")
    bt.insert(i)
    print(bt)
