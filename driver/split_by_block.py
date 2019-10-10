import math
import traceback
import json
import shutil
from configure import *  

class Block:
       def __init__ (self):
           self.min = UNIT*UNIT
	   self.max = 0

BLOCK_THRESHOLD = DIGIT_THRESHOLD - 6
def is_high_block(address):
    if len(address) < BLOCK_THRESHOLD:
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

def check_and_flush(address):
    global line_count, block_id, line_block
    if abs(prevAt - address) > BLOCK * PAGE_SIZE * PAGE_SIZE * PAGE_SIZE or line_count > BLOCK:
       filepath = LOG_DIR_PATH + FILENAME+"/block_"+str(block_id)+".csv"
       with open(filepath, 'w') as dump:
       	    for line in line_block:
       	        dump.write(line+"\n")
       line_block = []
       block_id += 1
       line_count = 0


if __name__ == "__main__": 
   global prevAt
   prevAt  = 0
   
   if len(sys.argv) < 2 or len(sys.argv) > 4:
      print "usage : python split_by_block.py --threshold [FILE TO CHOP]"
      exit(1)

   global FILENAME, ISTHRESHOLD

   if len(sys.argv) is 2:
      file = sys.argv[1]
      ISTHRESHOLD = False
   else :
      file = sys.argv[2]
      ISTHRESHOLD = True

   FILENAME = file.split("/")[-1].split(".")[0] 
   if ISTHRESHOLD:
      FILENAME=FILENAME+'_th'
 
   try : 
        line_count = 0
	block_id = 0
	line_block = []
	
        os.system('sudo mkdir -p ' + LOG_DIR_PATH + FILENAME)

   	with open(file, "r") as csv:
      	     for line in csv:
	         matched = is_valid_ms(line)
	         if matched is not None:
                    address = matched.group(2).strip()
		
		    if ISTHRESHOLD and BLOCK_THRESHOLD > len(address):
		       continue
                    address = int(address)
		    check_and_flush(address)
		    line_block.append(matched.group(1)+" "+str(address))
	    	    prevAt = address
	   	    line_count+=1

   except Exception as ex: 
         print ex
         if os.path.exists(LOG_DIR_PATH+FILENAME):
	    shutil.rmtree(LOG_DIR_PATH+FILENAME, ignore_errors=True)

