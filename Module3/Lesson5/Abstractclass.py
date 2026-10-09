from abc import ABC, abstractmethod

class ABSclass(ABC):
    def print(self, x):
        print("Pass value is: {}".format(x))
    @abstractmethod
    def task(self):
        print("I am inside ABS class")
class Subclass(ABSclass):
    def task(self):
        print("I am inside Subclass")
obj1 = Subclass()
obj1.print(10)
obj1.task()
