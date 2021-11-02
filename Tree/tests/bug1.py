from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)


print(f" ------------- Insert {1} ----------------")
bt.insert(1)
print(bt, "\n")


print(f" ------------- Insert {2} ----------------")
bt.insert(2)
print(bt, "\n")


print(f" ------------- Insert {3} ----------------")
bt.insert(3)
print(bt, "\n")

print(f"-------------- Delete {2} -----------------")
bt.delete(2)
print(bt)

print(f" ------------- Insert {4} ----------------")
bt.insert(4)
print(bt, "\n")
