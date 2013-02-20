# file: rw.py

"""Make drawing of repeated random walks using random colors
for each walk. Execute with 'python3 rw.py'"""


from turtle import *
from random import randint, uniform


def random_move(turtle, distance):
  """turn turtle through random angle and move forward by random distance"""
  angle = uniform(-90,90)
  d = uniform(0,distance)
  turtle.left(angle)
  turtle.forward(d)
  
def randcolor():
  """return random color --- a 3-tupe"""
  return (randint(0,255), randint(0,255), randint(0,255))
  
def gohome(turtle):
  """send turtle home without leaving a track."""
  turtle.penup()
  turtle.goto(0,0)
  turtle.pendown()

def random_walk(turtle, distance, steps):
  """Send turtle on random walk."""
  turtle.color(randcolor(), randcolor())
  for step in range(0,steps):
    random_move(turtle, distance)  
  gohome(turtle)

def repeat(steps, trials):
  """Repeat random_walk."""
  for trial in range(0,trials):
    random_walk(fred, 5, steps)

def saveImage(turtle, filename):
  """Save drawing to eps file."""
  ts = turtle.getscreen()
  tc = ts.getcanvas()
  tc.postscript(file=filename)
  
fred = Turtle()
fred.speed("fastest")
colormode(255)
N = 2000

fred.dot(10, "black")
repeat(2000, 20)

saveImage(fred, "fred1234.eps")
exitonclick()
