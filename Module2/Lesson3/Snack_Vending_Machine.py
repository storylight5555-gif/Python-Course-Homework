def calculate_change(amountpaid, price):
    change = amountpaid - price
    return change

snack_price = 45
print("The snack costs around", snack_price, "Dhirhams")
print("The accepeted coins are 1, 5, 10, 25 Dirhams")
total_amount = 0
number_of_coins = 0
while True:
    coin = int(input("Please insert a coin: "))
    if coin != 1 and coin != 5 and coin != 10 and coin != 25:
        print("Invalid coin. Please insert a valid coin.")
        continue
    total_amount= total_amount + coin
    number_of_coins += 1
    print("Total amount inserted:", total_amount, "Dhirhams")
    print("Number of coins inserted:", number_of_coins)
    if total_amount >= snack_price:
        print("You have inserted enough money to buy the snack.")
        break
change_due = calculate_change(total_amount, snack_price)
print("Dispensing snack...")
if change_due == 0:
    pass
else:
    print("Dispensing change of", change_due, "Dhirhams")
print("------------Purchase Bill------------")
print("Snack Price:", snack_price, "Dhirhams")
print("Total Amount Inserted:", total_amount, "Dhirhams")
print("Change Due:", change_due, "Dhirhams")
print("Coins Inserted:", number_of_coins)
print("Thank you for your purchase!")
print("Have a great day!")
print("------------End of Bill------------")
