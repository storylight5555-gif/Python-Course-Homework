import random
while True:
    user_input=input("Enter your choice (rock, paper, scissors): ")
    possible_actions=["rock", "paper", "scissors"]
    computer_choice=random.choice(possible_actions)
    print(f"\nYou chose {user_input}, computer chose {computer_choice}.\n")
    if user_input==computer_choice:
        print(f"Both players selected {user_input}. It's a tie!")
    elif user_input=="rock":
        if computer_choice=="scissors":
            print("Rock smashes scissors! You win!")
        else:
            print("Paper covers rock! You lose.")
    elif user_input=="paper":
        if computer_choice=="rock":
            print("Paper covers rock! You win!")
        else:
            print("Scissors cuts paper! You lose.")
    elif user_input=="scissors":
        if computer_choice=="paper":
            print("Scissors cuts paper! You win!")
        else:
            print("Rock smashes scissors! You lose.")
    play_again=input("Play again? (y/n): ")
    if play_again!="y":
        break