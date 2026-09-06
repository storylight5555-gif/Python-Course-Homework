items=["Pens", "Notebooks", "Erasers", "Rulers"]
stock_counts = [50, 30, 0, 20]
inventory = {item: count for item, count in zip(items, stock_counts)}
print("Full Inventory:", inventory)
in_stock_item = [item for item in items if inventory[item] > 0]
print("Items in Stock:", in_stock_item)


chosen_item = input("Enter the item you want to buy: ")
if chosen_item not in inventory:
    print(f"Sorry, {chosen_item} is not there in the inventory.")
    exit()
if inventory[chosen_item] == 0:
    print(f"Sorry, {chosen_item} is not available in stock.")
    exit()
price=[2, 5, 3, 8]
markup=int(input("Enter the markup value: "))
marked_up_prices = list(map(lambda x: x + markup, price))
print("Marked up prices:", marked_up_prices)
item_index=items.index(chosen_item)
print(f"The chosen item at this location is {item_index} ")
item_price=marked_up_prices[item_index]
print(f"The price of {chosen_item} item is AED {item_price}")
inventory[chosen_item] -= 1
print(f"Updated inventory after selling {chosen_item}:", inventory)
print("------ITEM BILL------")
print(f"Item: {chosen_item}")
print(f"Price: AED {item_price}")
print(f"Updated Inventory: {inventory}")
print("---------------------")