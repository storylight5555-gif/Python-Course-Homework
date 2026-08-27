list=[4,6,7,9,3,10,1,2]
print(list)
sum=0
for i in list:
    sum=sum+i
avg=sum/len(list)
print("sum=", sum)
print("avg=", avg)
list.sort()
print(list)
print("The smallest element is ", list[0] )
print("The bigesst element is ", list[-1])