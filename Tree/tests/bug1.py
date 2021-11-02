from Tree.BalancedTree import BalancedTree
import random

bt = BalancedTree(2)

insert = [x for x in range(30)]
random.Random(4).shuffle(insert)

delete = [19, 22, 21, 27, 18, 26, 25, 17, 16, 8]

for key in insert:
    print(f" ------------- Insert {key} ----------------")
    bt.insert(key)
    print(bt, "\n")

for key in delete:
    print(f"-------------- Delete {key} -----------------")
    bt.delete(key)
    print(bt, "\n")

print("hi")

# Problem: Rotation with with two inner nodes over the root
