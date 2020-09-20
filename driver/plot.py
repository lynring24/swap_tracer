import os
import pandas as pd
import numpy as np
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

MICROSECOND = 1000000

class Tracker(object):
    def __init__(self, axis, data):
        self.axis = axis
        self.data = data
    
    def add_plot(self, row):
        x = [row[0], row[0]]
        y = [row[1], row[2]]

    def run(self):
        pool = Pool(processes=cpu_count())
        return pool.map(self.add_plot, self.data)


labels={'map':'swap-in','fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'create':'allocation'}
colors={'map': 'mediumseagreen', 'out':'skyblue', 'fault':'lightpink', 'create': 'darkorange', 'layout':'lightslategrey', 'handle_mm':'lightslategrey' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}

    #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
    #    hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
    #    hook['mode'] = 'create'
    #    joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    #joined['timestamp'] = joined['timestamp'].astype(int)
    #joined['address'] = joined['address'].astype(int)
            
def draw_view(dir_path, mean_time):
            
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None, usecols=[0,5])
    maps.columns = ['range','pathname']   
    maps['pathname'] = maps['pathname'].fillna('[Anon]') 
    
    #maps['range'] = maps['range'].apply(lambda value :  value.split('-'))
    maps = maps.join(maps['range'].str.split('-', expand=True).add_prefix('range'))
    maps['range0'] = maps['range0'].apply(lambda x: int(x, 16))
    maps['range1'] = maps['range1'].apply(lambda x: int(x, 16))
    maps = maps.drop('range', axis=1)
    maps['merge'] = (maps['pathname'].shift(-1) == '[Anon]') & (maps['range0'].shift(-1) == maps['range1']) & (maps['pathname'].str.contains('/lib/')==False)
 
    indexs = maps[maps['merge'] == True].index
    ####### TODO

    for index in indexs:
        under = index+1 
        if maps.iloc[under]['merge'] == False:
           maps.at[index, 'range1'] = maps.iloc[under]['range1']
           maps = maps.drop(under)

    ################
    UNUSED = ['/lib/', '[vsyscall]'] 
    UNUSED_START = maps[maps.pathname.str.contains(UNUSED[0])]['range0'].min()
    UNUSED_END = maps[maps.pathname.str.contains(UNUSED[0])]['range1'].max()
    # maps = maps[(maps.range1 <= UNUSED_START) | (UNUSED_END <= maps.range0)]
    # maps = maps[maps.pathname != UNUSED[1]].reset_index() 


    def shorted(x):
        if os.path.isabs(x):
           return os.path.basename(x).split('.')[0]
        else:
           return x
    ## pathname 
    maps['pathname'] = maps['pathname'].apply(lambda value : shorted(value))
    maps = maps.reset_index()
    maps = maps[['range0', 'range1', 'pathname']]
    maps.to_csv('./maps.csv')

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)
    keys = list( zip(maps.range0, maps.range1)) 
    layout = pd.Series(maps.pathname.values, index=keys).to_dict()

    def labelize(x):
        diff = None
        label = None 
        for key in sorted(layout):
            if key[0] <= x and  x <= key[1]: 
                return layout[key]
            ## x value is bigger than the segment 
            elif key[1] <= x: 
                diff = abs(x - key[1])
                label = layout[key]
            else: 
                if diff >= abs(x - key[0]):
                    label= layout[key]
                break
        return label 

    rsyslog['label'] = rsyslog['address'].apply(lambda x : labelize(x))
    rsyslog.to_csv('./labelized.csv')


    plt.legend()
    plt.figure(figsize=(20, 5))
    plt.suptitle('Virtual Address by timeline')

    # output
    print "\n$ save plot"
    def config_axis(index, start, end):
        fig, axis = plt.subplots()
        for name, group in rsyslog.groupby('mode'):
            axis.set_ylim(start, end)
            axis.plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])
        plt.savefig("{}/{}.png".format(dir_path, index), format='png', dip=100)
        axis.legend()
        if os.environ.get('DISPLAY','') != '':
           plt.show()

    for name, group in rsyslog.groupby('label'):
        if len(group.index) > 0:
            start = group.address.min()
            end = group.address.max()
            if start < end:
                print '=> generate {}.png'.format(name)
                config_axis(name, start, end)
                        
