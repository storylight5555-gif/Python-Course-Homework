# ord() function returns ASCII value

print(ord('A'))     # Output: 65

print(ord('a'))     # Output: 97

print(ord('0'))     # Output: 48

print(ord('@'))     # Output: 64


# chr() function converts ASCII back to character

print(chr(65))      # Output: A

print(chr(97))      # Output: a
# Get input from user

char = input("Enter a single character: ")


# Validate: Check if exactly one character

if type(char) is str and len(char) == 1:

    print("Valid input!")

else:

    print("Please enter exactly ONE character!")
    # Get ASCII value

ascii_val = ord(char)


# Display the result

print(f"Character: {char}")

print(f"ASCII Value: {ascii_val}")
# Identify character type using ASCII ranges

if ascii_val >= 65 and ascii_val <= 90:

    print("Type: Uppercase Letter")

elif ascii_val >= 97 and ascii_val <= 122:

    print("Type: Lowercase Letter")

elif ascii_val >= 48 and ascii_val <= 57:

    print("Type: Digit")

elif ascii_val == 32:

    print("Type: Space")

else:

    print("Type: Special Character")
    # ASCII Value Checker - Complete Program


print("ASCII Value Checker")

print("=" * 40)

 
# Get input

char = input("Enter a single character: ")

 
# Validate input

if type(char) is str and len(char) == 1:

    # Get ASCII value

    ascii_val = ord(char)

    

    # Display results

    print(f"\nCharacter: '{char}'")

    print(f"ASCII Value: {ascii_val}")

    

    # Identify type

    print("\nCharacter Type: ", end="")

    if ascii_val >= 65 and ascii_val <= 90:

        print("Uppercase Letter")

    elif ascii_val >= 97 and ascii_val <= 122:

        print("Lowercase Letter")

    elif ascii_val >= 48 and ascii_val <= 57:

        print("Digit")

    elif ascii_val == 32:

        print("Space")

    else:

        print("Special Character")

else:

    print("\nError: Please enter exactly ONE character!")