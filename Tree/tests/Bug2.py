from Tree.BalancedTree import BalancedTree

bt = BalancedTree(2)

insert = [1]

delete = [1]

for key in insert:
    # print(f" ------------- Insert {key} ----------------")
    bt.insert(key)
    # print(bt, "\n")

for key in delete:
    # print(f"-------------- Delete {key} -----------------")
    bt.delete(key)
    print(bt, "\n")

print("hi.")
