# Pet Profile Builder
 
# PART 1: Create a simple class
class Pet:
    print("Hi, I am a pet profile class!")
 
# PART 2: Create an object from the class
pet_object = Pet()
 
 
# PART 3: Create a class with the __init__ method
class PetProfile:
 
    # class attribute
    category = "pet"
 
    # instance attributes
    def __init__(self, name, animal_type, age, favourite_food):
        self.name = name
        self.animal_type = animal_type
        self.age = age
        self.favourite_food = favourite_food
 
# PART 4: Create objects from the PetProfile class
pet1 = PetProfile("Buddy", "Dog", 4, "Biscuits")
pet2 = PetProfile("Milo", "Cat", 3, "Fish")
 
# PART 5: Access class attributes
print("Buddy is a {}".format(pet1.category))
print("Milo is also a {}".format(pet2.category))
 
# PART 6: Access instance attributes
print("{} is a {} and is {} years old.".format(pet1.name, pet1.animal_type, pet1.age))
print("{} likes eating {}.".format(pet1.name, pet1.favourite_food))
 
print("{} is a {} and is {} years old.".format(pet2.name, pet2.animal_type, pet2.age))
print("{} likes eating {}.".format(pet2.name, pet2.favourite_food))
