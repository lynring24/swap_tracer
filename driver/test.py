import re 
from datetime import datetime 

line="Wed Oct 23 18:22:41 2019"
pattern="%a %b %d %H:%M:%S %Y"
datetime.strptime(line, pattern) 
