Basket1={"apples", "oranges", "grapes", "bananas"}
Basket2={"pears", "kiwis", "mangoes", "bananas"}
print("Basket 1:", Basket1)
print("Basket 2:", Basket2)
Basket1.add("pears")
print("Basket 1 after adding 'pears':", Basket1)
common_fruits=Basket1.intersection(Basket2)
print("Common fruits in both baskets:", common_fruits)

import array as a
count=a.array('i',[1,2,3,4,5])
print("Array:", count)
count.append(7)
print("Array after appending 7:", count)
count.insert(5, 6)
print("Array after inserting 6 at index 4:", count)
count.append(3)
print("The count of 3 in the array:", count.count(3))
print(count)
count.reverse()
print(count)
