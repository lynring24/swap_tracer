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

def plot_out(dir_path, mean_time):
    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)

    
    min_range = len(str(rsyslog['timestamp'].min()))-1
    max_range = len(str(rsyslog['timestamp'].max()))+1
    
    binx = [pow(10, x) for x in range(min_range, max_range)]
    rsyslog['labelx'] = pd.cut(x=rsyslog['timestamp'], bins=binx)  
    subxranges = [ [group.timestamp.min(), group.timestamp.max()] for name, group in rsyslog.groupby('labelx') ]
    subxranges = [ x for x in subxranges if x != [] ]

    #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
    #    hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
    #    hook['mode'] = 'create'
    #    joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    #joined['timestamp'] = joined['timestamp'].astype(int)
    #joined['address'] = joined['address'].astype(int)
               

    digits = len(str(rsyslog['address'].min()))-1
    min_range = int(str(rsyslog['address'].min())[:-1*digits])*pow(10, digits)
    max_range = (int(str(rsyslog['address'].max())[:-1*digits])+2)*pow(10, digits)
    POW = pow(10, digits-2)
    biny = [ y for y in range(min_range, max_range, POW)]
    rsyslog['labely'] = pd.cut(x=rsyslog['address'], bins=biny)  
    
    subyranges = [ [group.address.min(), group.address.max()] for name, group in rsyslog.groupby('labely') ]
    subyranges = pd.DataFrame(subyranges).replace([np.inf, -np.inf], np.nan).dropna().values.tolist()
    subyranges = [ y for y in subyranges if y != [] ]

    if os.path.isfile('{}/maps'.format(dir_path)) == True:
        maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
        maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
        maps['pathname'] = maps['pathname'].fillna('anon')
        
        maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('address'))
        maps = maps.drop('layout', 1)
        maps['address0'] = maps['address0'].apply(lambda x: int(x, 16)) 
        maps['address1'] = maps['address1'].apply(lambda x: int(x, 16)) 
        maps  = maps[['address0','address1','pathname']]
        maps = maps.drop_duplicates()
            
    grids = [len(subxranges), len(subyranges)]
    fig, axes = plt.subplots(ncols=grids[0], nrows=grids[1])
    if grids[0]==1 and grids[1]==1:
        axes = [axes]
    if grids[0] == 1 or grids [1] ==1:
        axes = [axis for axis in axes]
    else:
        sorted_axes = []
        for idy in range(0, grids[1]):
            for idx in range(0, grids[0]):
                sorted_axes.append(axes[idy][idx]) 
        axes = sorted_axes
    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
        axis.spines['right'].set_visible(False)
        axis.spines['left'].set_visible(False)
    
    #fig.tight_layout()
    #fig.subplots_adjust(left=0.1)
    
    #layout = plt.twinx()
    #layout.spines["left"].set_position(('axes', 1.2))
    #make_patch_spines_invisible(layout)
    #layout.spines['left'].set_visible(True)

    rect_end = rsyslog['timestamp'].max()

        
    for idy in range(0, grids[1]):
        for idx in range(0, grids[0]):
            for name, group in rsyslog.groupby('mode'):
                axes[idy*grids[0]+idx].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])

            #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
            #    for index, rows in hook.iterrows():
            #        axes[idy*grids[0]+idx].add_patch(mpl.patches.Rectangle((rows['timestamp'], rows['address']), (rect_end - rows['timestamp']), rows['size'], color=colors['create'], label=labels['create'],zorder=0))

            converty = grids[1]-(idy+1)
            axes[idy*grids[0]+idx].set_xlim(subxranges[idx][0], subxranges[idx][1])
            axes[idy*grids[0]+idx].set_ylim(subyranges[converty][0], subyranges[converty][1])

            if idx == 0: 
                axes[idy*grids[0]+idx].spines['left'].set_visible(True)
            elif idx == grids[0] -1:
                axes[idy*grids[0]+idx].spines['right'].set_visible(True)
                axes[idy*grids[0]+idx].set_yticks([])
            else:
                axes[idy*grids[0]+idx].set_yticks([])

            if idy == 0:
                axes[idy*grids[0]+idx].spines['top'].set_visible(True)
                axes[idy*grids[0]+idx].set_xticks([])
            elif idy == grids[1] -1:
                axes[idy*grids[0]+idx].spines['bottom'].set_visible(False)
            else:
                axes[idy*grids[0]+idx].set_xticks([])

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass to plot, just so we don't keep repeating them
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    axes[0].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    kwargs.update(transform=axes[1].transAxes)  # switch to the bottom axes
    axes[1].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=axes[2].transAxes)  # switch to the bottom axes
    axes[2].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    kwargs.update(transform=axes[3].transAxes)  # switch to the bottom axes
    axes[3].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    kwargs.update(transform=axes[2].transAxes)  # switch to the bottom axes
    axes[2].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    kwargs.update(transform=axes[3].transAxes)  # switch to the bottom axes
    axes[3].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    kwargs.update(transform=axes[2].transAxes)  # switch to the bottom axes
    axes[2].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    kwargs.update(transform=axes[3].transAxes)  # switch to the bottom axes
    axes[3].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

         
                        
    plt.legend()
    plt.rcParams["figure.figsize"] = (14, 14)
    plt.suptitle('Virtual Address by timeline')
    #axes[int(len(subyranges)/2)][0].set_xlabel('timestamp')
    #axes[len(subyranges)-1][int(grids[0]/2)].set_ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png', dip=100)
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

