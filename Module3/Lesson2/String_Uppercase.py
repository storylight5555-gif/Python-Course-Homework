class IOString:
    def __init__(self):
        self.string = ""

    def get_string(self):
        self.string = input("Enter a string: ")

    def print_string(self):
        print(self.string.upper())
upercase_string = IOString()
upercase_string.print_string()
upercase_string.get_string()
upercase_string.print_string()