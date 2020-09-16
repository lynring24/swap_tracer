import os
import pandas as pd
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

    
    max_range = len(str(rsyslog['timestamp'].max()))+1
    min_range = len(str(rsyslog['timestamp'].min()))-1
    binx = [pow(10, x) for x in range(min_range, max_range)]
    rsyslog['labelx'] = pd.cut(x=rsyslog['timestamp'], bins=binx)  
    subxranges = [ [group.address.min(), group.address.max()] for name, group in rsyslog.groupby('labelx') ]
    subxranges = [ x for x in subxranges if x != [] ]

    #if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
    #    hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
    #    hook['mode'] = 'create'
    #    joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    #joined['timestamp'] = joined['timestamp'].astype(int)
    #joined['address'] = joined['address'].astype(int)
               
    subyranges=[]
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
        subyranges.extend(maps[['address0','address1']].values.tolist())

    else:
        max_range = len(str(rsyslog['address'].max()))+1
        min_range = len(str(rsyslog['address'].min()))-1

        biny = [pow(10, x) for x in range(min_range, max_range)]
        rsyslog['labely'] = pd.cut(x=rsyslog['address'], bins=biny)
        subyranges = [ [group.address.min(), group.address.max()] for name, group in rsyslog.groupby('labely') ]
        subyranges = [ y for y in subyranges if y != [] ]
            
    grids = [len(subxranges), len(subyranges)]
    fig, axes = plt.subplots(ncols=grids[0], nrows=grids[1])
    if grids[0]==1 and grids[1]==1:
        axes = [axes]
    if grids[0] == 1 or grids [1] ==1:
        axes = [axis for axis in axes]
    else:
        axes = [ axis for sub in axes for axis in sub ] 
    print grids
    print axes
    
    #fig.tight_layout()
    #fig.subplots_adjust(left=0.1)
    
    #layout = plt.twinx()
    #layout.spines["left"].set_position(('axes', 1.2))
    #make_patch_spines_invisible(layout)
    #layout.spines['left'].set_visible(True)

    rect_end = rsyslog['timestamp'].max()
        
    for idx in range(0, grids[0]):
        for idy in range(0, grids[1]):
            print idx, idy, idx*grids[0]+idy
            for name, group in rsyslog.groupby('mode'):
                axes[idx*grids[0]+idy].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])

            if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
                for index, rows in hook.iterrows():
                    axes[idx*grids[0]+idy].add_patch(mpl.patches.Rectangle((rows['timestamp'], rows['address']), (rect_end - rows['timestamp']), rows['size'], color=colors['create'], label=labels['create'],zorder=0))

            converty = grids[1]-(idy+1)
            axes[idx*grids[0]+idy].set_xlim(subxranges[idx][0], subxranges[idx][1])
            axes[idx*grids[0]+idy].set_ylim(subyranges[converty][0], subyranges[converty][1])

            if idx == 0: 
                axes[idx*grids[0]+idy].spines['right'].set_visible(False)
            elif idx == grids[0] -1:
               axes[idx*grids[0]+idy].spines['left'].set_visible(False)
               #axes[idx*grids[0]+idy].set_yticks([])
            else:
               axes[idx*grids[0]+idy].spines['left'].set_visible(False)
               axes[idx*grids[0]+idy].spines['right'].set_visible(False)
                #axes[idx*grids[0]+idy].set_yticks([])

            if idy == 0:
                axes[idx*grids[0]+idy].spines['bottom'].set_visible(False)
                #axes[idx*grids[0]+idy].set_xticks([])
            elif idy == grids[1] -1:
               axes[idx*grids[0]+idy].spines['top'].set_visible(False)
            else:
               axes[idx*grids[0]+idy].spines['top'].set_visible(False)
               axes[idx*grids[0]+idy].spines['bottom'].set_visible(False)    
                #axes[idx*grids[0]+idy].set_xticks([])
         
                        
    plt.legend()
    plt.suptitle('Virtual Address by timeline')
    #axes[int(len(subyranges)/2)][0].set_xlabel('timestamp')
    #axes[len(subyranges)-1][int(grids[0]/2)].set_ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png', dip=100)
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

