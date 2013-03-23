"""
histo.py: produce a histogram of word frequencies for the
given file.  

Usage:

  % python histo.py raven.txt 

  % python histo.py raven.txt -j junkwords.txt 

The first produces a histogram of raven.txt.  The second does the same
after removing the words in junkwords.txt  
"""
import sys, string, re

def string2file(s,filename):
  """
  Write a string to the given file.
  """
  file = open(filename,'w')
  file.write(s)
  file.close()

def file2string(path):
  """
  Get the contents of the file at path and return 
  it as a string.
  """
  file = open(path,'r')
  text = file.read()
  file.close()
  return text

def tally(key, dict):
  """Increase value of key by one if key is present,
  otherwise add the key and set its value to 1"""
  if key in dict:
    dict[key] = dict[key] + 1
  else:
    dict[key] = 1

def histogram(words):
  """
  Return a historgram (dictionary) of word 
  frequencies from the given list.
  """
  histo = { }
  for w in words:
    tally(w, histo)
  return histo

def get_words(text):
  """Return a list of words after cleaning up the text."""
  text = text.lower()
  T = text.maketrans('', '', string.punctuation)
  text = text.translate(T)
  T = text.maketrans('', '', string.digits)
  text = text.translate(T)
  return text.split()

def list_minus(A,B):
  """Return list of items in A which are not in B."""
  C = [ ]
  for item in A:
    if item not in B:
      C.append(item)
  return C

def junk_filter(word_list, junk_word_file):
  """Retun word_list minus words in the junk_word_file."""
  junkwords = file2string(junk_word_file)
  junk_words_list = junkwords.split()
  print("%d junk words read" % len(junk_words_list))
  return list_minus(words, junk_words_list)

def sort_table(T):
  """Sort table by tuple item 1."""
  p1 = lambda x: -x[1]
  T.sort(key=p1)

def relative_frequencies(table):
  """Given table of pairs (item, frequency), return table of 
  triples (item, frequeny, relative frequency)"""
  newtable = [ ]
  N = len(words)
  for item in table:
    f = 100*item[1]/N
    newitem = item + (f,)
    newtable.append(newitem)
  return newtable

def print_table(T):
  """Print table with summary."""
  for entry in T:
    print("%15s %3d   %4.3f" % tuple(entry))
  print("Number of unique words: %d" % len(table))

def write_output(name, T):
  """Write output for table T to file."""
  output_filename = sys.argv[1]+'.histo'
  output = ""
  for entry in table:
    output_entry = "%15s %3d   %4.3f" % tuple(entry)
    output = output + output_entry + '\n'
  string2file(output, output_filename)
  print("Look in %s for full histogram" % output_filename)

#############################################

text = file2string(sys.argv[1])              # open text file
words = get_words(text)                      # get word list

if (len(sys.argv) > 2) \
& (sys.argv[2] == "-j"):                     # filter out junk words
  words = junk_filter(words, sys.argv[3])
  
h = histogram(words)                         # make dictionary of word frequencies
table = list(h.items())                      # convert dictionary to a list
sort_table(table)                            # sort the list
table = relative_frequencies(table)          # compute relative frequencies

print_table(table[:20])                      # output to terminal  -- top 20 words
write_output(sys.argv[1]+'.histo', table)    # output to file      -- everything
