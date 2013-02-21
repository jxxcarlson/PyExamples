# Draw n-rayed fractal star using recursion
# Usage:
#
#   % python3 star.py 4 3 cross -- draw 4-pointed fractal star of depth 3
#                          -- save image in file named "cross3.eps"
#   % python3 star.py 4 3       -- as above, but do not save image
#
# Language: Python 3.3
# Author: J. Carlson
# Date: 2/19/2013
#
# REQUIRES: utilities.py -- from this repository
#
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

f = 0.3  # rescaling factor
    
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

# Draw a fractal star of depth sys.argv[2] with sys.argv[1] rays:
recursive_star(fred, int(sys.argv[1]), 200, int(sys.argv[2]))
fred.hideturtle()

# If there are enough arguments, save the image:
if len(sys.argv) == 4:
  saveImage(fred, sys.argv[3]+sys.argv[2]+".eps")
  
exitonclick()  
    
