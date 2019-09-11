import sys
import re

UNIT=1024*1024*1024
def init_range():
    return [1024*UNIT, 0]


if __name__ == "__main__" :
   unit=init_range()
   low=init_range()
   high=init_range()

   flag=0
   pattern=".+:.+:\d{2}(.+)"
   with open(sys.argv[1], "r") as csv:
      for line in csv:
          matched= re.compile(pattern).search(line)

          if matched is None:
              continue

          address=matched.group(1).strip()
          if len(address)!=flag: 
             # print unit
              unit=init_range()
              flag=len(address)

          address=int(address)
          if address < unit[0]:
              unit[0]=address
              if address < 100*UNIT:
                  if address < low[0]:
                     low[0]=address
              else:
                  if address < high[0]:
                      high[0]=address
              
          if address > unit[1]:
              unit[1]=address 
              if address < 100*UNIT:
                  if address > low[1]:
                      low[1]=address
              else:
                  if address > high[1]:
                      high[1]=address
  
print low , high
