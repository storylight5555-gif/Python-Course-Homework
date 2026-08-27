weather=(0,1,1,0,0,0,0,1)
rainy_weather=0
sunny_weather=0
for i in range(0,7):
    if(weather[i]==0):
        rainy_weather+=1
    else:
        sunny_weather+=1
if sunny_weather>rainy_weather:
    print("Good weather!")
else:
    print("Bad weather")