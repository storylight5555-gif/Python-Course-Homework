try:
    num1, num2 = eval(input("Enter two numbers separated by a comma: "))
    result = num1 / num2
    print("The result of division is:", result)
except ZeroDivisionError:
    print("Error: Division by zero is not allowed.")
except SyntaxError:
    print("Error: Invalid input format. Please enter two numbers separated by a comma.")
except:
    print("An unexpected error occurred.")
else:
    print("Division operation completed successfully.")
finally:
    print("Thank you for using the division calculator.")
    