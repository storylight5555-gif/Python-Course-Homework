class point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return "({0},{1})".format(self.x, self.y)
point1 = point()
point2 = point(10, 20)
print(point1)
print(point2)
