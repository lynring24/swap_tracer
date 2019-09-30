import os
import sys
import re
import math

BLOCK = 1024
PAGE_SIZE = 4096
DIGIT_THRESHOLD = 10

class Block:
       def __init__ (self):
           self.min = UNIT*UNIT
	   self.max = 0



def is_high_block(address):
    if len(address) < DIGIT_THRESHOLD:
       return False

    address = int(address)
    if address > high.max:
       high.max = address

    if address < high.min:
       high.min = address
    
    return True
  
     
def get_valid_range(lines):
   high = Block()
   high_lines = [] 
   for line in lines :

       address = matched.group(2).strip()
       if is_high_block(address) :
          high_lines.append(address)
   return high_lines
