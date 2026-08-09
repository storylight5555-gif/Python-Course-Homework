base= int(input("Enter the base number: "))
n= int(input("Enter the exponent number: "))

result = 1
for exponent in range(1, n + 1):
    result=1
    result = result * base
    print(f"{base} ^ {exponent} = {result}")