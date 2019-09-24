import os
import sys
import re
import traceback
import json

UNIT = 1024*1024*1024
BLOCK = 1024
PAGE_SIZE= 4096


# cut of the plot 
def flush(block, timestamp):  
    with open("../log/"+timestamp, 'w') as output
         output.write(json.dump(block))

if __name__ == "__main__" :
   previousAt  = 0
   path = path.rstrip(os.sep)
   global filename
   filename = os.path.basename(sys.argv[1])
   
   try : 
        count = 0
	os.system('mkdir ../log/'+filename)

	line_block = []
   	with open(sys.argv[1], "r") as csv:
      	     for line in csv:
 		 pattern="(.+:.+:\d{2}\.\d{6}) (.+)"
          	 matched= re.compile(pattern).search(line)

                 if matched is None:
                    continue

                 address = matched.group(2).strip()
                 address=int(address)
 		 if asb(previousAt - address) > 1024 * UNIT or count > BLOCK:
		    flush (line_block, matched.group(1).strip())
		    
		 line_block.append(matched.group(1)+" "+str(int(address /PAGE_SIZE)))
		 previousAt = address
		 count+=1
   except: 
        traceback.print_exec()
