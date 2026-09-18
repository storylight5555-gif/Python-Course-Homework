class Employee:

    def __init__(self):
        print("Employee created")

    def __del__(self):
        print("Destructor called, Employee deleted.")

def display():
    print("Making object...")
    emp=Employee()
    print("Function end")
    return emp


print("Calling display function...")
emp = display()
print("Program End")