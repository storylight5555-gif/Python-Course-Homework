field1=629
field2=743
field3=857
field4=912
field5=100
total = field1 + field2 + field3 + field4 + field5
average= total / 5
print("Total harvest is:", total,"kgs")
print("Average harvest is:", average,"kgs")
price_per_kg= 15
total_earnings= total * price_per_kg
print("Total earnings are:", total_earnings,"AED")
bags_size=25
total_bags= total // bags_size
print("Total bags needed are:", total_bags)
total_leftover= total % bags_size
print("Total leftover harvest is:", total_leftover,"kgs")
last_year=4923
print("better than last year", total > last_year)
print("same as last year", total == last_year)
print("atleast as good as last year", total >= last_year)
print("worse than last year", total < last_year)
total+= 30
print("Total harvest after adding 30 kgs is:", total,"kgs")
total-= 15
print("Total harvest after removing 15 kgs is:", total,"kgs")
updated_bags= total // bags_size
print("Updated total bags needed are:", updated_bags)