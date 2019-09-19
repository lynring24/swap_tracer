import os
import sys
import re

UNIT = 1024*1024*1024
BLOCK = 1024
PAGE_SIZE= 4096

def flush():
    




if __name__ == "__main__" :
   previousAt  = 0
   path = path.rstrip(os.sep)
   global filename
   filename = os.path.basename(sys.argv[1])
   
   try : 
        count = 0
	os.system('mkdir ../plot/'+filename)

	line_block = []
   	with open(sys.argv[1], "r") as csv:
      	     for line in csv:
 		 pattern="(.+:.+:\d{2}\.\d{6}) (.+)"
          	 matched= re.compile(pattern).search(line)

                 if matched is None:
                    continue

                 address = matched.group(2).strip()
                 address=int(address)
 		 if asb(previousAt - address) < 1024 * UNIT :
		    line_block.append(matched.group(1)+" "+str(int(address /PAGE_SIZE)))
		 else :
       		    date_pattern = "%Y-%m-%dT%H:%M:%S.%f"
		    time = datetime.strptime(matched.group(1), date_pattern) 
		    flush (line_block, time:wq!)
		 previousAt = address
