# Draw n-rayed fractal star using recursion
# Language: Python 3.3
# Author: J. Carlson
# Date: 2/19/2013
# Site for images: square-the-circle.com

import sys 
from utilities import saveImage
from turtle import *


def star(turtle, n,r):
  """ draw a star of n rays of length d"""
  for k in range(0,n):
    turtle.pendown()
    turtle.forward(r)
    turtle.penup()
    turtle.backward(r)
    turtle.left(360/n)

f = 0.3
    
def recursive_star(turtle, n, r, depth):
  """At each point of the star, draw another smaller star,
  and so on, up to given depth.  Rescale the stars by a factor f
  at each generation."""
  global f
  if depth == 0:
    star(turtle, n, f*4)
  else:
    for k in range(0,n):
      turtle.pendown()
      turtle.forward(r)
      recursive_star(turtle, n, f*r, depth - 1)
      turtle.penup()
      turtle.backward(r)
      turtle.left(360/n)
 
 
fred = Turtle()
fred.speed("fastest")
# star(fred, 20, 100) # draw a 20-star

# Draw a fractal cross of depth 4:
recursive_star(fred, 6, 200, int(sys.argv[1]))
fred.hideturtle()
saveImage(fred, "snofwlake2.eps")
exitonclick()  
    
