from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)

for key in range(10, 30):
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt, "\n")

delete = [22, 20]
for key in delete:
    print(f"-------------- Delete {key} -----------------")
    bt.delete(key)
    print(bt, "\n")

