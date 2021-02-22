



from datetime import datetime 
import sys
import subprocess

CMD = sys.argv[1]

START_TIME = datetime.now()

p = subprocess.Popen(CMD, shell=True)
p.wait()

END_TIME = datetime.now()

print("time elapsed (s) : {}".format((END_TIME - START_TIME).total_seconds()))

