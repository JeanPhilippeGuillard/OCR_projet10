sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8]
pairs = filter(lambda x: x % 2 ==0, sequence)
impairs = filter(lambda x: x % 2 != 0, sequence)
print(f"Nombres pairs : {list(pairs)}")
print(f"Nombres impairs : {list(impairs)}")

my_list = iter(["Tesla model 3", "VW ID4", "Cupra El Born"])
print(my_list)
print(type(my_list))
x = next(my_list)
print(x)

print("list(pairs) :", list(pairs))
print([0, 2, 4, 6, 8])
my_list = iter(list(pairs))
my_list = iter([0, 2, 4, 6, 8])

print(my_list)
print(type(my_list))
x = next(my_list)
print(x)