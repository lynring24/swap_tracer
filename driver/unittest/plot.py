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

def string_to_date(timestamp):
    try: 
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S,%f')                                       
    return timestamp


labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'allocation':'allocation'}
colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'brown', 'handle_mm':'magenta' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}

def plot_out(dir_path, mean_time):
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
    maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
    maps['pathname'] = maps['pathname'].fillna('anon')
    
    maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('layout'))
    maps = maps.drop('layout', 1)
    maps['layout0'] = maps['layout0'].apply(lambda x: int(x, 16)) 
    maps['layout1'] = maps['layout1'].apply(lambda x: int(x, 16)) 
    maps  = maps[['layout0','layout1','pathname']]
    maps = maps.drop_duplicates()

    print maps.columns, len(maps.index)

    subyranges = maps[['layout0','layout1']].values.tolist()

    layout = dict() 
    for name, group in maps.groupby('pathname'):
        if name != 'anon':
            head = group.layout0.min()
            tail = group.layout1.max()
            layout[name] = [head, tail]


    # nsegment = sum(len(v) for v in layout.itervalues())
    nsegment = len(layout)
    # read hook.csv for this case

    hook = pd.read_csv(dir_path+"/hook.csv", sep='\s+',header=None)
    hook.columns=['timestamp', 'file', 'line','func','var','address','size']
    hook['timestamp'] = hook['timestamp'].apply(lambda x: (string_to_date(x) - string_to_date('2020-08-31T23:24:36.551695')).total_seconds() * MICROSECOND )
    hook = hook[hook.timestamp>= 0.0]
    hook['address'] = hook['address'].apply(lambda x :int(x, 16))
    hook['timestamp'] = hook['timestamp'].astype(int)
    joined = hook[['timestamp', 'address']]


    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog = rsyslog.query('cmd=="linear" & mode=="handle_mm"')
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)
    joined = pd.concat([hook[['timestamp', 'address']], rsyslog[['timestamp', 'address']]])
    joined.to_csv('./joined.csv')
    

    max_range = len(str(joined['timestamp'].max()))+1
    min_range = max(len(str(joined['timestamp'].min()))-1, 0)
    binx = [pow(10, x) for x in range(min_range, max_range)]
    joined['labelx'] = pd.cut(x=joined['timestamp'], bins=binx) 

    
    subxranges = []
    for name, group in joined.groupby('labelx'):
        if (len(group.index)) > 0:
            subxranges.append([max(group.timestamp.min(), 0)  , group.timestamp.max() + 10])
              
            
    fig, axes = plt.subplots(ncols=len(subxranges), nrows=nsegment)
   # fig.tight_layout()
    

    rect_end = joined['timestamp'].max()

    print "$ add data to plots"
        
    for idx in range(len(subxranges)-1,-1,-1):
        for idy in range(0, nsegment):
            plt.subplots_adjust(hspace =0.2)
            converty = len(subyranges)-(idy+1)
            axes[idy][idx].set_xlim(subxranges[idx][0], subxranges[idx][1])
            axes[idy][idx].set_ylim(subyranges[converty][0], subyranges[converty][1])
            #print idx, idy, subyranges[idy]

            for name, group in rsyslog.groupby('mode'):
                axes[idy][idx].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])
            #axes[idy][idx].plot(hook.timestamp, hook.address, c=colors['allocation'], marker='o', linestyle=' ', ms =10, zorder=10)
            for index, rows in hook.iterrows():
                axes[idy][idx].add_patch(mpl.patches.Rectangle((rows['timestamp'], rows['address']), (rect_end - rows['timestamp']), rows['size'], color=colors['allocation'], label=labels['allocation'],zorder=0))
                        
    plt.legend()
    plt.suptitle('Virtal Address by timeline')
    plt.xlabel('timestamp')
    plt.ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png', dip=100)
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

plot_out('.', 0)
