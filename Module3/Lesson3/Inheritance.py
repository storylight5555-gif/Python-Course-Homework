class family_member:
    def __init__(self, eye_color, hair_color, height):
        self.eye_color = eye_color
        self.hair_color = hair_color
        self.height = height
    def show_traits(self):
        print(f"Eye Color: {self.eye_color}, Hair Color: {self.hair_color}, Height: {self.height}")
class child(family_member):
    def __init__(self, name, age, eye_color, hair_color, height):
        self.name = name
        self.age = age
        super().__init__(eye_color, hair_color, height)
    def show_traits(self):
        print(f"Name: {self.name}, Age: {self.age}")
        super().show_traits()
    def favorite_hobby(self, hobby):
        print(f"{self.name}'s favorite hobby is {hobby}.")
obj1 = child("Krishna", 11, "Brown", "Black", 120)
obj1.show_traits()
obj1.favorite_hobby("Drawing")
print("is child a subclass of family_member?", issubclass(child, family_member))
