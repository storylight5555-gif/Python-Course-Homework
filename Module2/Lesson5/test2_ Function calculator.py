print("-------------------------------")
print("--Welcome to your Calculator!--")
print("-------------------------------")
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero is not allowed."
    return x / y

try:
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    operation = input("Choose operation (+, -, *, /): ")

    if operation == '+':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif operation == '-':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif operation == '*':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif operation == '/':
        print(f"{num1} / {num2} = {divide(num1, num2)}")
    else:
        print("Invalid operation! Please choose from +, -, *, /.")
except ValueError:
    print("Invalid input! Please enter numeric values.")
except ZeroDivisionError:
    print("Error! Division by zero is not allowed.")
