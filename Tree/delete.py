from Tree.BalancedTree import BalancedTree

bt = BalancedTree(1)

keys = [1, 22, 21, 12, 3, 11, 50, 60, 70, 80, 90, 100, 110, 120, 130]

for key in keys:
    bt.insert(key)
    print(f" ------------- Insert {key} ----------------")
    print(bt)

print(" ------------- Delete 11 ---------------- delete leaf")
bt.delete(11)
print(bt)

print(" ------------- Delete 110 ---------------- delete from internal node")
bt.delete(110)
print(bt)

print(" ------------- Delete 130 ---------------- delete from internal node, all children minimal number of keys")
bt.delete(130)
print(bt)

print(" ------------- Delete 90 ---------------- ")
bt.delete(90)
print(bt)

print(" ------------- Delete 1 ---------------- merge ")
bt.delete(1)
print(bt)

print("test")
