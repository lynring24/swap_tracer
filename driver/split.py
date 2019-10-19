import math
import json
import shutil
from common import *  

class Block:
       def __init__ (self):
           self.min = UNIT*UNIT
	   self.max = 0


def is_high_block(vpn):
    if len(vpn) < get_threshold('pvn'):
       return False

    vpn = int(vpn)
    if vpn > high.max:
       high.max = vpn

    if vpn < high.min:
       high.min = vpn
    
    return True
  
     
def get_valid_range(lines):
   high = Block()
   high_lines = [] 
   for line in lines :

       vpn = matched.group(2).strip()
       if is_high_block(vpn) :
          high_lines.append(vpn)
   return high_lines




def check_and_flush(vpn):
    global line_count, block_id, line_block
    page_size = get_size('PAGE')
    block_size = get_size('BLOCK')
    interval = page_size * page_size * page_size * block_size
    if abs(prevAt - vpn) > interval or line_count > block_size:
       filepath = get_path('block')+str(block_id)+".csv"
       with open(filepath, 'w') as dump:
       	    for line in line_block:
       	        dump.write(line+"\n")
       line_block = []
       block_id += 1
       line_count = 0


def split():
   global prevAt
   prevAt  = 0

   try : 
        line_count = 0
	block_id = 0
	line_block = []
	

   	with open(get_path('extracted'), 'r') as csv:
      	     for line in csv:
	         matched = is_valid_ms(line)
	         if matched is not None:
                    vpn = matched.group(2).strip()
	            # threshold is enable and block_treshold > len(vpn)	
		    if do_threshold() and get_threshold() > len(vpn):
		       continue
                    vpn = int(vpn)
		    check_and_flush(vpn)
		    line_block.append(matched.group(1)+" "+str(vpn))
	    	    prevAt = vpn
	   	    line_count+=1

   except Exception as ex: 
         print ex
         if os.path.exists(get_path('block')):
	    shutil.rmtree(get_path('block'), ignore_errors=True)

