secret=27
print("Welcome to the secret number game!")
print("Try to guess the secret number between 1 and 50.")
print("You have 5 attempts to guess the number.")
if __name__ == "__main__":
    attempts = 5
    while attempts > 0:
        guess = int(input("Enter your guess: "))
        if guess < 1 or guess > 50:
            print("Please enter a number between 1 and 50.")
            continue
        if guess == secret:
            print("Congratulations! You've guessed the secret number!")
            break
        elif guess <= secret:
            print("cold! Try again.")
        elif guess - secret < -10:
            print("ice cold! Try again.")
        elif guess > secret:
            print("warm! Try again.")
        elif guess - secret < 10:
            print("hot! Try again.")
        attempts -= 1
        print(f"You have {attempts} attempts left.")
    else:
        print(f"Sorry, you've used all your attempts. The secret number was {secret}.")