"""sm.py: Stack machine.  

AT THE COMMAND LINE:
  
    See introduction to sm.py:
    $ python3 sm.py 
  
    Run simple example in silent mode
    # python3 -s sm.py 1 2 add
    
    Run simple example in verbose mode (default)
    # python3 sm.py 1 2 add
    ================================= 
    code: ['1', '2', 'add']
    --------- 
    token: 1
    stack: [1]
    --------- 
    token: 2
    stack: [1, 2]
    --------- 
    token: add
    in exop, stack: [1, 2, 'add']
    stack: [3]
    ============== 
    3 
    
INTERACTIVE MODE:
  
  # turn verbose mode off for testing
  # turn it on using 'verbose_on()' to see stack trace
  >>> verbose_off()
  
  # instruction set -- binary functions  
  >>> run("1 2 add")
  3
  >>> run("1 2 sub")
  -1
  >>> run("2 3 mul")
  6
  >>> run("3 2 div")
  1.5
  
  # builtin constant
  >>> run("pi")
  3.131459265
  
  # builtin unary function
  >>> run("1.5 int")
  1
  
  # many instructions:
  >>> run("2 3 add 2 mul 2 div 1 sub")
  4.0
  
  # variables
  >>> run("3 a sto a rcl")
  3
  
  # use of (builtin) function
  >>> # compute sum of squares of 3 and 4
  >>> run("3 a sto 4 b sto a rcl square b rcl square add")
  25
  
  # halt machine
  >>> run("1 2 halt add")
  'halt'
  
  # unknown instructions 'ignored' -- just pushed to stack
  >>> run("1 2 foo bar")
  'bar'
  
  # stack instructions
  >>> run("3 dup mul")
  9
  
  # define function as code --- can be pushed onto stack and executed
  >>> # define doubling function, apply it to 7:
  >>> run("defcode db 2 mul /defcode 7 db") 
  14
  
  # defined function as prog --- execute each instruction using interpreter
  >>> # define 'cube' which cubes its argument
  >>> run("defprog cube dup dup mul mul /defprog 3 cube")
  27
  
  To add new instructions, add entries to the dictionary 'opTable',
  then add the corresponding function.  See, for example, how the 
  functions 'add' (binary), 'int' (unary), and 'pi' (0-ary) are 
  implemented. 
"""

import sys

"""
Contents:

  - Documentation
  - Instruction set

"""
##########################################################
# DOCUMENTATION
##########################################################  

message = """ 
  COMMAND LINE:
  python3 sm.py 1 2 add       -- simple example, command line
  python3 sm.py -s 1 2 add    -- same, silent (verbose = off)
  python3 sm.py -t            -- internal test
  python3 sm.py -d            -- print documentation

  INTERACTIVE:
  $ python3
  >>> from sm import *
  >>> verbose_off()          -- verbose_on() sets verbosity to default value
  >>> run('1 2 add')         -- example, interactive mode
  >>> ex(['1', '2', 'add'])  -- same example, list input
  
  Use 'verbose_on() to see stack trace

  have a nice day
  """

##########################################################
# INSTRUCTION SET
##########################################################

def add(stack):
  """Pop top two values of stack, add them, push result onto stack."""
  val = stack.pop() + stack.pop()
  stack.append(val)
 
def mul(stack):
  """Pop top two values of stack, multiply them, push result onto stack."""
  val = stack.pop() * stack.pop()
  stack.append(val)

def sub(stack):
  """Pop top two values of stack, subtract second from first, push result onto stack."""
  a = stack.pop()
  b = stack.pop()
  val = b - a
  stack.append(val)
  
def div(stack):
  """Pop top two values of stack, divide second by first, push result onto stack."""
  denom = stack.pop()
  num = stack.pop()
  val = num / denom
  stack.append(val)
  
def INT(stack):
  """Pop top values of stack, take integer part, push result onto stack."""
  stack.append(int(stack.pop()))
  
def pi(stack):
  """Push value of pi onto stack."""
  stack.append(3.131459265)

def dup(stack):
  """Put copy of top value of stack onto stack."""
  stack.append(top(stack))
  
def sto(stack):
  """Pop stack[top], stack[top-1].  Install stack[top-1] in opTable,
  set value to ('var', stack[top]).
  # STACK: 7 A sto <top>"""
  var = stack.pop()
  val = ('var', stack.pop())
  opTable[var] = val
  
def rcl(stack):
  """Pop top of stack, let op be the result.  Push opTable[op][1] onto stack."""
  # STACK: A <top> ==> STACK: 7 <top>
  op = stack.pop()
  opVal = opTable[op]
  stack.append(opVal[1])
    
def report(stack):
  """Print the stack."""
  print("STACK:", stack)

def popstack(stack):
  """Pop stack."""
  stack.pop()
  
def show_opTable(stack):
  """print operator table."""
  for key in opTable:
    print(key, opTable[key])
    
def clear_op(stack):
  """Pop name from stack and clear it from the operator table."""
  key = stack.pop()
  opTable.pop(key, None)

def clear_stack(stack):
  """Clear the stack."""
  stack = []
  
# DICTIONAY WHICH DEFINES THE INSTRUCTION SET.  KEYS ARE INSTRUCTIONS (STRINGS).
# VALUES ARE PAIRS: A TUPLE WHOSE FIRST ELEMENT GIVES THE INSTRUCTION TYPE
# AND WHOSE SECOND ELEMENT IS A FUNCTION.
opTable = {'sto':('stack', sto), 'rcl':('stack', rcl), 'dup': ('stack', dup),
        'report':('stack', report), 'pop':('stack', popstack), 'clear_op':('stack', clear_op),
        'show_opTable':('stack', show_opTable), 'clear_stack':('stack', clear_stack),
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

def vprint(verbose, x, y):
  if verbose:
    print(x,y)

def top(stack):
  if len(stack) > 0:
    return stack[-1]
  else:
    return "NONONO!"
    
def is_executable(op):
  if op not in opTable:
    return False
  opType, opValue = opTable[op]
  if opType == 'var':
    return False
  else:
    return True

def evaluate(x):
  if x[0].isalpha():
    return x
  elif x.find(".") > -1:
    return float(x)
  else:
    return int(x)
    
def pushvector(v, stack):
  """Push the elements of the vector (list, tuple) onto the stack."""
  for element in v:
    stack.append(element)
    
def exprog(prog, stack):
  """Execute the program 'prog'."""
  global verbose
  
  stack.pop()
  i = 0
  while i < len(prog):
    op = prog[i]
    stack.append(op)
    vprint(verbose, "prog:", prog[i:])
    exop(stack)
    i = i + 1

def exstackop(operator, stack):
  stack.pop()
  operator(stack)

def excode(operator, stack):
  stack.pop()
  pushvector(operator, stack)

def ex_nothing(operator, stack):
  pass

ex_table = { }
ex_table['var'] = ex_nothing
ex_table['code'] = excode
ex_table['stack']= exstackop
ex_table['prog'] = exprog

def exop(stack):
  """Execute the operator which is at the top of the stack.
  Find the type of the operator, then dispatch """
  global verbose
  vprint(verbose, "in exop, stack:", stack)
  
  op = top(stack)
  operatorType, operator = opTable[op]
  f = ex_table[operatorType]
  f(operator, stack)
  
def excodedef(code, i):
  global verbose
  global opTable
  
  op = code[i+1]
  currentcode = code[i+1:]
  def_end = code.index('/defcode')  # BUG HERE!!
  codebody = list(map(evaluate, code[i+2:def_end]))
  i = def_end  # ADVANCE TO FIRST TOKEN BEYOND THE DEFINITION
  opTable[op] = ('code', codebody)
  vprint(verbose, "new op:", op)
  vprint(verbose, "codebody:", opTable[op])
  return i,def_end

def exprogdef(code, i):
  global verbose  
  global opTable
  
  op = code[i+1]
  currentcode = code[i+1:]
  def_end = code.index('/defprog')  # BUG HERE!!
  codebody = list(map(evaluate, code[i+2:def_end]))
  i = def_end  # ADVANCE TO FIRST TOKEN BEYOND THE DEFINITION
  
  vprint(verbose, "defcode, op", op)
  vprint(verbose, "defcode, codebody:", codebody)
  vprint(verbose, "remaining code", code[i:])
  
  opTable[op] = ('prog', codebody)
  
  vprint(verbose, "new op:", op)
  vprint(verbose, "codebody:", opTable[op])
  
  return i,def_end
          
def ex(code):
  """ex(code):  execute a list or tuple of strings representing instructions and data.
  Example: ex(['1', '2', 'add']) or ex(('1', '2', 'add'))."""
  global verbose
  global opTable
  vprint(verbose, "=================================", "")
  vprint(verbose, "code:", code)
  
  # SET UP STACK AND CODE POINTERS ip, def_end
  S = []
  ip = 0; def_end = 0
  
  # MAIN LOOP
  while (ip < len(code)) & (top(S) != 'halt'):
  
    # GET NEXT TOKEN
    token = code[ip]
    
    vprint(verbose, "---------", "")
    vprint(verbose, "token:", token)
    
    # PROCESS TOKEN: 

    if token == 'defcode':
      ip,def_end = excodedef(code,ip)
    elif token == 'defprog':
      ip,def_end = exprogdef(code,ip)
    else:
      S.append(evaluate(token))
     
    # EXECUTE STACK
    while is_executable(top(S)) & (top(S) != 'halt'):
      exop(S)
    vprint(verbose, "stack:", S) 
    
    # ADVANCE TOKEN CURSOR AND ENSURE THAT 
    # IT IS TO THE RIGHT OF THE LAST DEFINITION PROCESSED
    ip = ip + 1
    if def_end > ip:
      ip = def_end
    
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

def set_verbosity(b):
  """set_verbosity(b): set global verbosity flag (True/False)."""
  global verbose
  verbose = b

def verbose_on():
  """verbose_on(): set global verbosity flag to True."""
  set_verbosity(True)
  
def verbose_off():
  """verbose_off(): set global verbosity flag to False."""
  set_verbosity(False)
  
def _test():
    verbose_off()
    import doctest
    doctest.testmod()

def print_docstring():
  import sm
  print(sm.__doc__)

      
##########################################################
# MAIN
##########################################################

# Table of functions versus options
option_table = { }
option_table['-t'] = _test
option_table['-d'] = print_docstring
option_table['-v'] = verbose_on
option_table['-s'] = verbose_off

def run_option(arg):
  arg = sys.argv[1]
  if arg in option_table:
    f = option_table[arg]
    f()

def ex_input(input):
  result = ex(input)
  print(result)

def process_args(arglist):
  if len(arglist) == 0:
    return None
  arg = arglist[0]
  if arg[0] == "-":
    run_option(arg)
    process_args(arglist[1:])
  else:
    code = arglist
    ex_input(code)

if __name__ == "__main__": 
  verbose_on() # default

  # SELF TEST (runs docstring at head of module):
  from doctest import testmod
  import sm
  testmod(sm)
  
  # PROCESS ARGS:
  if len(sys.argv) == 1:
    print(message)
  else:
    process_args(sys.argv[1:])
 
    
    


