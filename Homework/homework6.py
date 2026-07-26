a = input("Enter the first value (A): ")
b = input("Enter the second value (B): ")
c = input("Enter the third value (C): ")

print(f"\nBefore swapping: A = {a}, B = {b}, C = {c}")

temp = a
a = c
c = b
b = temp

print(f"After swapping:  A = {a}, B = {b}, C = {c}")