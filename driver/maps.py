import pandas as pd
import numpy as np
from math import ceil, isnan

MICROSECOND = 1000000



def convert(address):
    address = address & 0xFFFFFFFF
    if address & 0x80000000:
        address = -((~address & 0xFFFFFFFF) + 1)



def map():
    print "$ extract process map"
    maps = pd.read_csv('./maps', header=None, delimiter='\s+')
    maps.columns = ['range','mode', 'offset', 'dev','indoe','pathname']
    maps = maps.join(maps['range'].str.split(',', expand=True).add_prefix('range'))
    maps = maps.apply(lambda row: convert(row['range0']) convert(row['range1']),axis=1)
    maps.to_csv('./maps.csv')

map()



        


         

