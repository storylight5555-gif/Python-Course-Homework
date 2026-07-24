print("-------------------------------")
print("   WELCOME TO RIDE BUILDER     ")
print("-------------------------------")

print("Step 1 select your vehicle.")
print("1-Bike")
print("2-Car")
print()
choice=int(input("Enter 1 or 2:"))
if choice==1:
    print("Step 2, pick your bike type.")
    print("1-Scooty")
    print("2-Mountain bike")
    print()
    Bike_type=int(input('Enter 1 or 2:'))
    print()
    if Bike_type==1:
        print("You picked: The Scooty")
        print("Top Speed: 80 km/hr")
        print("Best for: City roads") 
    elif Bike_type==2:
        print("You picked: The Mountain Bike")
        print("Top Speed:  140 km/hr")
        print("Best for: Ofroad Trails ")
    else:
        print("This is not a valid choice")
        print("Enter 1 or 2")
    print()
    print("-----------------------------------------------")
    print("Your custom ride is ready!\nEnjoy the journey!")
    print("-----------------------------------------------")
elif choice==2:
    print("Step 2, pick your car type.")
    print("1-Sedan")
    print("2-SUV")
    print()
    Car_type=int(input('Enter 1 or 2:'))
    print()
    if Car_type==1:
        print("You picked: Sedan")
        print("Seats : 5 passengers")
        print("Best for : family trips ")
    elif Car_type==2:
        print("You picked: SUV")
        print("Seats : 7 passengers")
        print("Best for : adventure trips ")
    else:
        print("This is not a valid choice")
        print("Enter 1 or 2")
    print()
    print("-----------------------------------------------")
    print("Your custom ride is ready!\nEnjoy the journey!")
    print("-----------------------------------------------")
else:
    print("This is not a valid choice")
    print("Enter 1 or 2")
    print("Try again")
    