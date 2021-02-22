import os
import pandas as pd
import sys

log = pd.read_csv(sys.argv[1], header=None, sep='\s+')

log.columns = ['pid' ,'usr', 'pr','ni', 'virt', 'res','shr', 's', 'cpu', 'mem','duration', 'command']
#log = log[log['command']=='bzip2_base.gcc4']

log['res'] = log['res'].apply(lambda x : float(x[:-1])*1024*1024 if 'g' in str(x) else float(x))

print( log.head(6))
log['physic'] = log.apply(lambda row:(row['res'] + row['shr']), axis = 1) 
#log['physic'] = log.apply(lambda row:(row['res'] + row['shr'])/1024, axis = 1) 
#log['virt'] = log['virt'].apply(lambda x : x/1024)
print( " MAX (MiB)", log.virt.max()/1024, log.physic.max())



