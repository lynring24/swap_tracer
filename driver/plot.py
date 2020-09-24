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
colors={'map': 'mediumseagreen', 'fault': 'orangered', 'out':'skyblue', 'create': 'darkorange', 'layout':'lightslategrey', 'handle_mm':'lightslategrey' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}

    #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
    #    hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
    #    hook['mode'] = 'create'
    #    joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    #joined['timestamp'] = joined['timestamp'].astype(int)
    #joined['address'] = joined['address'].astype(int)
            
 
PADDING = 5*pow(10,5)
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
    for index in indexs:
        under = index+1 
        if maps.iloc[under]['merge'] == False:
            maps.at[index, 'range1'] = maps.iloc[under]['range1']
            maps = maps.drop(under) 

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



    # output
    print "\n$ save plot"

    def break_axis(index, segments):
        if index != 'landscape':
            plt.figure(figsize=(14,4))            


        digits = len(str(segments['timestamp'].min()))-1
        min_range = int(str(segments['timestamp'].min())[:-1*digits])*pow(10, digits)
        max_range = (int(str(segments['timestamp'].max())[:-1*digits])+2)*pow(10, digits)
        POW = pow(10, digits-2)
        binx = [ x for x in range(min_range, max_range, POW)]
        segments['labelx'] = pd.cut(x=segments['timestamp'], bins=binx)   
        subxranges = [ [group.address.min(), group.address.max()] for name, group in segments.groupby('labelx') ]
        subxranges = pd.DataFrame(subxranges).replace([np.inf, -np.inf], np.nan).dropna().values.tolist()
        subxranges = [ x for x in subxranges if x != [] ]

        digits = len(str(segments['address'].min()))-1
        min_range = int(str(segments['address'].min())[:-1*digits])*pow(10, digits)
        max_range = (int(str(segments['address'].max())[:-1*digits])+2)*pow(10, digits)
        POW = pow(10, digits-2)
        biny = [ y for y in range(min_range, max_range, POW)]
        segments['labely'] = pd.cut(x=segments['address'], bins=biny)                          
        subyranges = [ [group.address.min(), group.address.max()] for name, group in segments.groupby('labely') ]
        subyranges = pd.DataFrame(subyranges).replace([np.inf, -np.inf], np.nan).dropna().values.tolist()
        subyranges = [ y for y in subyranges if y != [] ]
        

        GRIDS = len(subyranges)
        fig, axes = plt.subplots(nrows=GRIDS)
        
        if GRIDS==1:
            axes = [axes]
        else:
            axes = [axis for axis in axes]

        # set spines false
        for axis in axes:
            axis.spines['bottom'].set_visible(False)
            axis.spines['top'].set_visible(False)
        

        d = .015  # how big to make the diagonal lines in axes coordinates
        kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
            
        for idy in range(0, GRIDS):
            for name, group in segments.groupby('mode'):
                axes[idy].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])

            converty = GRIDS-(idy+1)
            axes[idy].set_ylim(subyranges[converty][0]-PADDING, subyranges[converty][1]+PADDING)

            if idy == 0:
                axes[idy].spines['top'].set_visible(True)
                #axes[idy].set_xticks([])
            # for case there are only one axis 
            if idy == GRIDS-1:
                axes[idy].spines['bottom'].set_visible(True)

            if idy != GRIDS-1: 
                axes[idy].set_xticks([])

            if idy == 0:
                axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
                axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
            else:
                kwargs.update(transform=axes[idy].transAxes)  # switch to the bottom axes
                axes[idy].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                axes[idy].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
                axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
                axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal                        
        plt.suptitle('Virtual Address by timeline in /{}'.format(index))
        plt.savefig("{}/{}.png".format(dir_path, index), format='png', dip=100)
        axis.legend()
        if os.environ.get('DISPLAY','') != '':
            plt.show()


    for name, group in rsyslog.groupby('label'):
        if len(group.index) > 0:
            print name, len(group)
            start = group.address.min()
            end = group.address.max()
            if start < end:
                print '=> generate {}.png'.format(name)
                break_axis(name, group)

    print "=> generate landscape.png"
    break_axis('landscape', rsyslog)

