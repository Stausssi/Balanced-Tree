from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)

keys = [1, 22, 21, 12, 3, 11, 50, 60, 70, 80, 90, 100, 110, 120, 130]

for key in keys:
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt)

node, key = bt.search(21)
print(bt.get_in_order_successor(node, key))
print(bt.get_in_order_predecessor(node, key))
