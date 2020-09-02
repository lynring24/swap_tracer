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


labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'create':'allocation'}
colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'create':'brown', 'handle_mm':'magenta' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}

def plot_out(dir_path, mean_time, command):

    #if os.path.isfile('{}/maps'.format(dir_path)) == True:
        #maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
        #maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
        #maps['pathname'] = maps['pathname'].fillna('anon')
        
        #maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('layout'))
        #maps = maps.drop('layout', 1)
        #maps['layout0'] = maps['layout0'].apply(lambda x: int(x, 16)) 
        #maps['layout1'] = maps['layout1'].apply(lambda x: int(x, 16)) 
        #maps  = maps[['layout0','layout1','pathname']]
        #maps = maps.drop_duplicates()

        #subyranges = maps[['layout0','layout1']].values.tolist()

        #layout = dict() 
        #for name, group in maps.groupby('pathname'):
        #    if name != 'anon':
        #       head = group.layout0.min()
        #       tail = group.layout1.max()
        #       layout[name] = [head, tail]


        # nsegment = sum(len(v) for v in layout.itervalues())
        #segment = len(layout)
        # read hook.csv for this case

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog = rsyslog.query('cmd=="linear"')
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)
    # kernel address is already set for integer 
    joined = rsyslog[['timestamp', 'address', 'mode']]

    if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
        hook = pd.read_csv(dir_path+"/hook.csv", usecols=['timestamp', 'address','size'])
        hook['mode'] = 'create'
        joined = pd.concat([hook[['timestamp', 'address', 'mode']], joined[['timestamp', 'address', 'mode']]])
    joined['timestamp'] = joined['timestamp'].astype(int)
    joined['address'] = joined['address'].astype(int)
    joined.to_csv('./joined.csv')
    
    max_range = len(str(joined['timestamp'].max()))+1
    min_range = min(len(str(joined['timestamp'].min()))-1, 0)

    binx = [pow(10, x) for x in range(min_range, max_range)]
    joined['timestamp'] = joined['timestamp'].astype(int)
    joined['labelx'] = pd.cut(x=joined['timestamp'], bins=binx) 

    
    subxranges = []
    for name, group in joined.groupby('labelx'):
        if (len(group.index)) > 0:
            subxranges.append([max(group.timestamp.min(), 0)  , group.timestamp.max() + 10])
              
    max_range = len(str(joined['address'].max()))+1
    min_range = min(len(str(joined['address'].min()))-1, 0)

    biny = [pow(10, x) for x in range(min_range, max_range)]
    joined['labely'] = pd.cut(x=joined['address'], bins=biny) 
 
    subyranges = []
    for name, group in joined.groupby('labely'):
        if (len(group.index)) > 0:
            subyranges.append([max(group.address.min(), 0)  , group.address.max() + 10])
            
    fig, axes = plt.subplots(ncols=len(subxranges), nrows=len(subyranges))
    fig.tight_layout()

    rect_end = joined['timestamp'].max()
        
    for idx in range(len(subxranges)-1,-1,-1):
        for idy in range(len(subyranges)-1, -1, -1):
            plt.subplots_adjust(hspace =0.2)
            # converty = len(subyranges)-(idy+1)
            axes[idy][idx].set_xlim(subxranges[idx][0], subxranges[idx][1])
            axes[idy][idx].set_ylim(subyranges[idy][0], subyranges[idy][1])

            if idx == 0: 
                axes[idy][idx].spines['right'].set_visible(False)
            elif idx == len(subxranges) -1:
                axes[idy][idx].spines['left'].set_visible(False)
            else:
                axes[idy][idx].spines['left'].set_visible(False)
                axes[idy][idx].spines['right'].set_visible(False)

            if idy == 0: 
                axes[idy][idx].spines['bottom'].set_visible(False)
            elif idy == len(subyranges) -1:
                axes[idy][idx].spines['top'].set_visible(False)
            else:
                axes[idy][idx].spines['top'].set_visible(False)
                axes[idy][idx].spines['bottom'].set_visible(False)

            for name, group in rsyslog.groupby('mode'):
                axes[idy][idx].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])
            
         
            if os.path.isfile('{}/hook.csv'.format(dir_path)) == True:
                for index, rows in hook.iterrows():
                    axes[idy][idx].add_patch(mpl.patches.Rectangle((rows['timestamp'], rows['address']), (rect_end - rows['timestamp']), rows['size'], color=colors['create'], label=labels['create'],zorder=0))
                        
    plt.legend()
    plt.suptitle('Virtual Address by timeline')
    plt.xlabel('timestamp')
    plt.ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png', dip=100)
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

