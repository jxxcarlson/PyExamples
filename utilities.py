# file: utitlties.py
# Author: J. Carlson
# Date: Feb 19, 2013

def saveImage(turtle, filename):
  """Save turtle graphics drawing to eps file."""
  ts = turtle.getscreen()
  tc = ts.getcanvas()
  tc.postscript(file=filename)
