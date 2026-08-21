try:
    num=int(input("Enter a number: "))
    print("You entered:", num)
except ValueError as e:
    print("Invalid input. Please enter a valid integer.")
    print("Error:", e)
