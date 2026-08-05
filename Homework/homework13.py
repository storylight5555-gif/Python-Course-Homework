import turtle

screen = turtle.Screen()
screen.bgcolor("white")
screen.title("Dharani's Square Design")

t = turtle.Turtle()
t.shape("turtle")
t.color("red")
t.pensize(5)
t.speed(3)

for _ in range(4):
    t.forward(150)
    t.right(90)

screen.exitonclick()