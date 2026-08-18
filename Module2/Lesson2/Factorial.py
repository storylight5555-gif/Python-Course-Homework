def factorial(num):
    '''Calculate the factorial of a given number.'''
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial(num - 1)
print(factorial.__doc__)
print("the factorial of 5 is:", factorial(5))
print("the factorial of 0 is:", factorial(0))
print("the factorial of 3 is:", factorial(3))
print("the factorial of 2 is:", factorial(2))