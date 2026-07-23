print("Enter your marks of 5 subjects.")
m1=int(input("Subject 1: "))
m2=int(input("Subject 2: "))
m3=int(input("Subject 3: "))
m4=int(input("Subject 4: "))
m5=int(input("Subject 5: "))
total=m1+m2+m3+m4+m5
avg= int (total/5)
validrange=range(1,101)
print("Total marks ",total,"Avg", avg)
if avg not in validrange:
    print("Invalid input.")
elif avg in range(91, 101):
    print("Grade: A")
elif avg in range(81, 91):
    print("Grade: B")
elif avg in range(71, 81):
    print("Grade: C")
elif avg in range(61, 71):
    print("Grade: D")
else:
    print("Grade: F")