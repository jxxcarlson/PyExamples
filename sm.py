"""sm.py: Stack machine
  Examples:

  >>> from sm import *
  >>> run("1 2 add")
  3
  >>> run("2 3 add 2 mul 2 div 1 sub")
  4.0
  >>> run("3 a sto a rcl")
  3 
  >>> # define 'cube' which cubes its argument
  >>> run("defprog cube dup dup mul mul /defprog 3 cube")
  27
  >>> # compute sum of squares of 3 and 4
  >>> run("3 a sto 4 b sto a rcl square b rcl square add")

  Say set_vebosity(True) to see stack machine in operation
  Say set_verbosity(False) to see results only 
"""

import sys

##########################################################
# DOCUMENTATION
##########################################################

def _print(x):
  print(); print(" ", x)
  
def print_documentation():
  _print("FUNCTIONS:")
  _print(set_verbosity.__doc__)
  _print(run.__doc__)
  _print(ex.__doc__)
  print()

##########################################################
# INSTRUCTION SET
##########################################################

def add(stack):
  val = stack.pop() + stack.pop()
  stack.append(val)
 
def mul(stack):
  val = stack.pop() * stack.pop()
  stack.append(val)

def sub(stack):
  a = stack.pop()
  b = stack.pop()
  val = b - a
  stack.append(val)
  
def div(stack):
  denom = stack.pop()
  num = stack.pop()
  val = num / denom
  stack.append(val)
  
def INT(stack):
  stack.append(int(stack.pop()))
  
def pi(stack):
  stack.append(3.131459265)

def dup(stack):
  stack.append(top(stack))
  
def sto(stack):
  # STACK: 7 A sto <top>
  var = stack.pop()
  val = ('var', stack.pop())
  ops[var] = val
  
def rcl(stack):
  # STACK: A <top> ==> STACK: 7 <top>
  op = stack.pop()
  opVal = ops[op]
  stack.append(opVal[1])
    
def report(stack):
  print(stack)

def popstack(stack):
  stack.pop()
  
def show_ops(stack):
  for key in ops:
    print(key, ops[key])
    
def clear_op(stack):
  key = stack.pop()
  ops.pop(key, None)

def clear_stack(stack):
  stack = []
ops = {'sto':('stack', sto), 'rcl':('stack', rcl), 'dup': ('stack', dup),
        'report':('stack', report), 'pop':('stack', popstack), 'clear_op':('stack', clear_op),
        'show_ops':('stack', show_ops), 'clear_stack':('stack', clear_stack),
       'add': ('stack', add), 'sub': ('stack', sub), 'mul': ('stack', mul), 'div': ('stack',div),
        'int': ('stack', INT), 'pi':('stack', pi), 'double':('code', [2, 'mul']),
         'square':('prog', ('dup', 'mul')) }

"""
Operator types:

stack: operates on the full stack
code: can be pushed onto the stack and then executed
prog: must be run through the interpreter one token at a time

Language: defcode, defprog
"""
##########################################################
# INTERPRETER
##########################################################

def pushvector(v, stack):
  for element in v:
    stack.append(element)
    
def exprog(prog, stack):
  global verbose
  
  stack.pop()
  i = 0
  while i < len(prog):
    op = prog[i]
    stack.append(op)
    vprint(verbose, "prog:", prog[i:])
    exop(stack)
    i = i + 1
    
def exop(stack):
  global verbose
  vprint(verbose, "in exop, stack:", stack)
  
  op = top(stack) 
  if op in ops:
    
    operatorType, operatorValue = ops[op]
   
    if operatorType == 'var':
      # stack.pop()
      # stack.append(operatorValue)
      # stack.append(op)
      # stack.append('halt')
      pass
    elif operatorType == 'code':
      op = stack.pop()
      pushvector(operatorValue, stack)
    elif operatorType == 'stack':
      stack.pop()
      operatorValue(stack)
    elif operatorType == 'prog':
      exprog(operatorValue, stack)
    else:
      print("error, unknown operator type")
      exit()
 
def excodedef(code, i):
  global verbose
  global ops
  
  op = code[i+1]
  currentcode = code[i+1:]
  j = code.index('/defcode')  # BUG HERE!!
  codebody = list(map(evaluate, code[i+2:j]))
  i = j  # ADVANCE TO FIRST TOKEN BEYOND THE DEFINITION
  ops[op] = ('code', codebody)
  vprint(verbose, "new op:", op)
  vprint(verbose, "codebody:", ops[op])
  return i,j

def exprogdef(code, i):
  global verbose  
  global ops
  
  op = code[i+1]
  currentcode = code[i+1:]
  j = code.index('/defprog')  # BUG HERE!!
  codebody = list(map(evaluate, code[i+2:j]))
  i = j  # ADVANCE TO FIRST TOKEN BEYOND THE DEFINITION
  
  vprint(verbose, "defcode, op", op)
  vprint(verbose, "defcode, codebody:", codebody)
  vprint(verbose, "remaining code", code[i:])
  
  ops[op] = ('prog', codebody)
  
  vprint(verbose, "new op:", op)
  vprint(verbose, "codebody:", ops[op])
  
  return i,j
      
def evaluate(x):
  if x[0].isalpha():
    return x
  elif x.find(".") > -1:
    return float(x)
  else:
    return int(x)
    
def vprint(verbose, x, y):
  if verbose:
    print(x,y)
  
def top(stack):
  if len(stack) > 0:
    return stack[-1]
  else:
    return "NONONO!"
    
def is_executable(op):
  if op not in ops:
    return False
  opType, opValue = ops[op]
  if opType == 'var':
    return False
  else:
    return True
    
def run(input):
  return ex(input.split(" "))
    
def ex(code):
  """ex(code):  execute a list or tuple of strings representing instructions and data.
  Example: ex(['1', '2', 'add']) or ex(('1', '2', 'add'))."""
  global verbose
  global ops
  vprint(verbose, "=================================", "")
  vprint(verbose, "code:", code)
  
  # SET UP STACK AND CODE POINTERS i, j
  S = []
  i = 0; j = 0
  
  # MAIN LOOP
  while (i < len(code)) & (top(S) != 'halt'):
  
    # GET NEXT TOKEN
    token = code[i]
    
    vprint(verbose, "---------", "")
    vprint(verbose, "token:", token)
    
    # PROCESS TOKEN

    if token == 'defcode':
      i,j = excodedef(code,i)
    elif token == 'defprog':
      i,j = exprogdef(code,i)
    else:
      S.append(evaluate(token))
     
    # EXECUTE STACK
    while is_executable(top(S)) & (top(S) != 'halt'):
      exop(S)
    vprint(verbose, "stack:", S) 
    
    # ADVANCE TOKEN CURSOR AND ENSURE THAT 
    # IT IS TO THE RIGHT OF THE LAST DEFINITION PROCESSED
    i = i + 1
    if j > i:
      i = j
    
  vprint(verbose, "==============", "")
  
  # LOOP IS COMPLETE, return value
  if len(S) > 0:
    return S.pop() 
  else:
    return None  
  
	
def run(input):
  """run(input): parse the input string and run the resulting code.
  Example: run('1 2 add')"""
  return ex(input.split(" "))
  	
##########################################################
# EXAMPLE PROGRAMS AND TESTS
##########################################################

verbose = True

def _test():
    global verbose
    verbose = False
    import doctest
    doctest.testmod()


def test_instructions():
  '''
  >>> run("1 2 add")
  3
  >>> run("1 2 sub")
  -1
  >>> run("2 3 mul")
  6
  >>> run("3 2 div")
  1.5
  >>> run("pi")
  3.131459265
  >>> run("1.5 int")
  1
  >>> run("2 3 add 2 mul 2 div 1 sub")
  4.0
  >>> run("3 a sto a rcl")
  3
  '''

def test_programs():
  '''
  >>> run("3 dup mul")
  9
  >>> # define doubling function, apply it to 7:
  >>> run("defcode db 2 mul /defcode 7 db") 
  14
  >>> # define 'cube' which cubes its argument
  >>> run("defprog cube dup dup mul mul /defprog 3 cube")
  27
  >>> # compute sum of squares of 3 and 4
  >>> run("3 a sto 4 b sto a rcl square b rcl square add")
  25
  '''
  
def set_verbosity(b):
  """set_verbosity(b): set global verbosity flag (True/False)."""
  global verbose
  verbose = b
    
##########################################################

message = """ 
  python3 sm.py 1 2 add      -- simple example, command line
  >>> run('1 2 add')         -- same example, interactive mode
  >>> ex(['1', '2', 'add'])  -- same example, list input
  
  python3 sm.py -e            -- more examples 
  python3 sm.py -t            -- internal test
  python3 sm.py -d            -- print documentation

  have a nice day
  """

##########################################################

if __name__ == "__main__": 
  set_verbosity(True) # default

  # GET INPUT FOR INTERPRETER
  if len(sys.argv) == 1:
    print(message)
  elif (len(sys.argv) == 2) & (sys.argv[1][0] == "-"):
    if sys.argv[1] == '-t':
      _test()
    elif sys.argv[1] == "-d":
      print_documentation()
    elif sys.argv[1] == "-e":
      print("\n  More examples.  These are the 'unit tests' run using 'python3 sm.py -t'")
      print("  >>> from sm import *")
      print(test_instructions.__doc__)
      print(test_programs.__doc__)
  else:
    code = sys.argv[1:]
    result = ex(code)
    print()
    print(result)
    print()

# pp rpn.py defprog cube dup dup mul mul /defprog 3 cube
# pp rpn.py defprog quad dup mul dup mul /defprog 3 quad
