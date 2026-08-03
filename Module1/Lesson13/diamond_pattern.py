rows=int(input("Enter number of rows: ")) #5
if rows % 2 == 0:
    d=rows//2
else:
    d=(rows//2)+1# d=3 
space=d-1# space=2
for i in range(1,d+1):# i=1
    for j in range(1,space+1):# range(1,3)
        print(" ",end="")
    space-=1# space=1
    for j in range(1,(2*i)):# range(1,2)
        print(j,end="")
    print()
space=1
for i in range(1,d):
    for j in range(1,space+1):
        print(" ",end="")
    space+=1
    for j in range(1,(2*(d-i))):# range(1,4)
        print(j,end="")
    print()