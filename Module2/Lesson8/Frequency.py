Dict1={"A": 2 , "B": 2 , "C": 2 , "D" : 1}
print("The original dictionary is ", Dict1)
count=0
for key in Dict1:
    if Dict1[key]==2:
        count=count+1
print("The frequency of 2 is ", count)
