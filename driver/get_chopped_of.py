import os
import sys
import re
import math
import traceback
import json
import shutil
import time, calendar
from datetime import datetime

BLOCK = 1024
PAGE_SIZE= 4096

def check_and_flush(address):
    global line_count, block_id, line_block
    if abs(previousAt - address) > BLOCK * PAGE_SIZE * PAGE_SIZE * PAGE_SIZE or line_count > PAGE_SIZE:
       filepath = "../log/"+filename+"/block_"+str(block_id)+".csv"
       for line in line_block:
           with open(filepath, 'w') as dump:
       	        dump.write(line)
       line_block = []
       block_id += 1
       line_count = 0
       print address


if __name__ == "__main__" :
   global previousAt
   previousAt  = 0
   global filename
   filename = sys.argv[1].split("/")[-1].split(".")[0]
   
   try : 
        line_count = 0
	block_id = 0
	line_block = []
	
	os.system('sudo mkdir -p ../log/'+filename)
   	with open(sys.argv[1], "r") as csv:
      	     for line in csv:
 		 pattern="(\d+:\d{2}:\d{2}\.\d{6}) (.+)"
          	 matched= re.compile(pattern).search(line)

                 if matched is None:
                    continue 
                 address = int(matched.group(2).strip())
		 check_and_flush(address)
		 line_block.append(matched.group(1)+" "+str(int(address /PAGE_SIZE)))
		 previousAt = address
		 line_count+=1

   except Exception as ex: 
         print ex
         if os.path.exists("../log/"+filename):
	    shutil.rmtree("../log/"+filename, ignore_errors=True)
