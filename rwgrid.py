"""Random walk of turtle on a square grid.
File: rwgrid.py
Usage:

    % python3 rwgrid.py

"""

from random import randint
from utilities import saveImage
from turtle import *

def rm(turtle, d):
  """random move (up, down, left, right) for turtle 
  by d pixels."""
  k = randint(0,1)
  if k == 0:
    turtle.lt(90)
  else:
    turtle.rt(90)
  turtle.forward(d)

def run(d, n):
  """run turtle."""
  fred = Turtle()
  fred.speed("fastest")

  for k in range(0, n):
    rm(fred, d)
    # print(k)

  fred.hideturtle()
  saveImage(fred, "random_walk.eps")


if __name__ == '__main__':
    run(10,2000)
    
    exitonclick()

