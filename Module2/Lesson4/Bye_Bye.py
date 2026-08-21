valid = False
while not valid:
    try:
        num = int(input("Enter a number: "))
        print("You entered:", num)
        while num%2==0:
            print("Bye Bye")
            break    
        valid = True
    except ValueError:
        print("Error: Please enter a valid integer.")