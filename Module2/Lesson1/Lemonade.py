def greet_customer():
    print("Welcome to Lemonade Stand!")
    print("We have fresh lemonade for you.")
greet_customer()
price_per_cup=float(input("Enter the price per cup of lemonade: "))
cups_sold=int(input("Enter the number of cups sold:"))
def calculate_total_sales(price_per_cup, cups_sold):
    total_sales = price_per_cup * cups_sold
    return total_sales

total_sales = calculate_total_sales(price_per_cup, cups_sold)
total_sales=round(total_sales, 2)
print(f"Total sales: ${total_sales}")
amount_paid=float(input("Enter the amount paid by the customer: "))
def calculate_change(amount_paid, total_sales):
    change = amount_paid - total_sales
    return change
change_due = calculate_change(amount_paid, total_sales)
change_due=round(change_due, 2)
print(f"Change due: ${change_due}")
def thank_you_message(cups_sold):
    if cups_sold >=5:
        return("Thank you for your bulk purchase! Enjoy your lemonade!")
    else:
        return("Thank you for your purchase! Enjoy your lemonade!")
closing_message = thank_you_message(cups_sold)
print(closing_message)

print("======== Lemonade Stand Receipt ========")
print(f"        Price per cup: ${price_per_cup}")
print(f"        Cups sold: {cups_sold}")
print(f"        Total sales: ${total_sales}")
print(f"        Amount paid: ${amount_paid}")
print(f"        Change due: ${change_due}")
print(          f"        {closing_message}")
print("=======================================")