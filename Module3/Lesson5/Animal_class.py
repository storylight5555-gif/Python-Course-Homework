from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def Move(self):
        pass
class Human(Animal):
    def Move(self):
        print("Human can walk and run")
class Snake(Animal):
    def Move(self):
        print("Snake can crawl")
class Shark(Animal):
    def Move(self):
        print("Shark can swim")
class Parrot(Animal):
    def Move(self):
        print("Parrot can fly")
obj1 = Human()
obj2 = Snake()
obj3 = Shark()
obj4 = Parrot()
obj1.Move()
obj2.Move()
obj3.Move()
obj4.Move()