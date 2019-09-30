import os
import sys
import re
import math
import traceback
import json
import shutil
from configure import *  

BLOCK = 1024
PAGE_SIZE= 4096
DIGIT_THRESHOLD = 8



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
      print "usage : python get_chopped_of.py --noise-cancel [FILE TO CHOP]"
      exit(1)

   global FILENAME, NOISE_CANCEL

   if len(sys.argv) is  2:
      file = sys.argv[1]
      NOISE_CANCEL = False
   else :
      file = sys.argv[2]
      NOISE_CANCEL = True

   FILENAME = file.split("/")[-1].split(".")[0] 
   if NOISE_CANCEL:
      FILENAME=FILENAME+'_nc'
 
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
		
		    if NOISE_CANCEL and DIGIT_THRESHOLD > len(address):
		       continue
                    address = int(address)
		    check_and_flush(address)
		    line_block.append(matched.group(1)+" "+str(int(address /PAGE_SIZE)))
		    prevAt = address
		    line_count+=1

   except Exception as ex: 
         print ex
         if os.path.exists(LOG_DIR_PATH+FILENAME):
	    shutil.rmtree(LOG_DIR_PATH+FILENAME, ignore_errors=True)
