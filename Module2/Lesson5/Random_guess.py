import random 
num = random.randint(0, 9)
print("Guess a number between 0 and 9")
print("The game will continue until you guess the correct number.")
valid = True 
while valid:
    guess = int(input("Enter your guess: "))
    if guess == num:
        print("Congratulations! You guessed the correct number.")
        print("The correct number was:", num)
        break
    else:
        print("Sorry, that's not the correct number. Try again!")
        