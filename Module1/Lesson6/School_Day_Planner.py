print("===== SCHOOL DAY PLANNER =====")
print("Answer 3 questions and I will plan your day for you!\n")

day=input("What day is it? (Monday to Sunday): ").capitalize()
weather=input("What is the weather? (sunny, rainy, cloudy): ").lower()
homework=input("Is your homework done? (yes/no): ").lower()

print("")
print("Here's your plan for " , day , "!")

# topic 1 -- if - elif - else classify the day
if day in ("Saturday", "Sunday"):
    print("Day type: Weekend enjoy your day off!")
elif day=="Monday":
    print("Day type: First day of the week pack your weekly planner.")
elif day=="Friday":
    print("Day type: Last school day return books to the library")
elif day in ("Tuesday", "Wednesday", "Thursday"):
    print("Day type: Regular school day stay focused ")
else:
    print("Day type: Invalid day entered please check your spelling.")

# topic 2 -- AND operator
if weather=="sunny" and homework=="yes":
    print("Weather: Sunny and homework is done! Enjoy your outdoor activities.")

# topic 3 -- OR operator
if weather=="rainy" or weather=="cloudy":
    print("Weather: Pack an umbrella and wear a raincoat.")

# topic 4 -- NOT operator
if not homework=="yes":
    print("Homework: Finish your homework before playing video games.")

# topic 5 -- combining AND, OR, and NOT operators
if (weather=="rainy") and not homework=="yes":
    print("Best plan: Stay indoors and complete your homework before going outside.")
elif (weather=="sunny") and homework=="yes" and not day in ("Saturday", "Sunday"):
    print("Best plan: All set for a great school day you are prepared")
elif day in ("Saturday", "Sunday") and weather=="sunny":
    print("Best plan: Enjoy your weekend outdoors!")
else:
    print("Best plan: Take it 1 step at a time, you have got this!")

print("")
print("Plan Complete Have a great day!")
