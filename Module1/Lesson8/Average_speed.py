a=int(input("Enter a value for a:"))
b=int(input("Enter a value for b:"))
c=int(input("Enter a value for c:"))
avg=(a+b+c)/3
print("Avg=", avg)

if avg > a and avg > b and avg > c:
    print(avg, "Is higher than ", a, ",", b,  ",", c )
elif avg > a and avg > b:
    print(avg, "Is higher than ", a, ",", b )
elif avg > a and avg > c:
    print(avg, "Is higher than ", a, ",", c )
elif avg > b and avg > c:
    print(avg, "Is higher than ", b, ",", c )
elif avg > a :
    print(avg, "Is higher than ", a )
elif avg > b :
    print(avg, "Is higher than ", b )
elif avg > c:
    print(avg, "Is higher than ", c )
else:
    print("Invalid input")