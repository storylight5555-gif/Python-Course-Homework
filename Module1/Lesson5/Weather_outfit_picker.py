temperature=int(input("Enter the temperature in Celsius: "))
if temperature < 20:
    outfit="jacket"
    print("It's cold today.")
    print("Wear a ", outfit)
else:
    outfit="t-shirt"
    print("It's warm today.")
    print("Wear a ", outfit)


is_raining=input("Is it raining? (yes/no): ")
if is_raining=="yes":
    print("Bring an umbrella.")

wind_speed=int(input("Enter the wind speed in km/h: "))
if wind_speed > 30:
    need_windbreaker=True
    print("It's windy today.")
    print("Consider wearing a windbreaker.")
else:
    need_windbreaker=False
    print("No windbreaker needed.")


is_puddles=input("Are there puddles on the ground? (yes/no)): ")
if is_puddles=="yes":
    shoes="boots"
    print("The ground is wet.")
    print("Wear ", shoes)
else:
    shoes="sneakers"
    print("The ground is dry.")
    print("Wear ", shoes)


print("\n Weather check complete.")
print("===== WEATHER OUTFIT PICKER SUMMARY =====")
print("Temperature: ", temperature, "°C")
print("Outfit: ", outfit)
print("Raining: ", is_raining)
print("Wind Speed: ", wind_speed, "km/h")
print("Need Windbreaker: ", need_windbreaker)
print("Shoes: ", shoes)