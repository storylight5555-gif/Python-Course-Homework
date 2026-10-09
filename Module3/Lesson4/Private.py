class Private:

    __private_var = 23
    def __private_method(self):
        print("This is a private method.")
    def hello(self):
        print("Accessing private variable:", self.__private_var)
        self.__private_method()
obj1=Private()
obj1.hello()
