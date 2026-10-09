class Computer:

    def __init__(self):
        self.__price = 900

    def sell(self):
        print("Selling Price: {}".format(self.__price))

    def setPrice(self, price):
        self.__price = price

obj1= Computer()
obj1.sell()
obj1.__price = 1000
obj1.sell()
obj1.setPrice(15000)
obj1.sell()