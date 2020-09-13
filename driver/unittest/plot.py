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
    address = pd.read_csv(dir_path+"/address", sep=':',header=None)
    address.columns=['pathname','hex0']
    address['hex0'] = address['hex0'].apply(lambda x: x.strip())
    address['hex1'] = address['hex0']
    address['dec0'] = address['hex0'].apply(lambda x: int(x, 16)) 
    address['dec1'] = address['hex1'].apply(lambda x: int(x, 16)) 
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
    maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
    maps['pathname'] = maps['pathname'].fillna('anon')
    
    maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('hex'))
    maps = maps.drop('layout', 1)
    maps['dec0'] = maps['hex0'].apply(lambda x: int(x, 16)) 
    maps['dec1'] = maps['hex1'].apply(lambda x: int(x, 16)) 
    maps  = maps[['dec0','dec1','pathname']]
    joined = pd.concat([address,maps])
    joined.to_csv('joined.csv')

    
    
    #maps = maps.drop_duplicates()
    #maps = maps[maps['pathname'].isin(['/home/hrchung/benchmarks/segment/report', 'anon', '[heap]','[stack]'])]

    subyranges = maps[['dec0','dec1']].values.tolist()

    # nsegment = sum(len(v) for v in layout.itervalues())
    # read hook.csv for this case

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog = rsyslog.query('mode=="fault"')
    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)

    # drop vsyscall data
    vsyscall = maps[maps.pathname == "[vsyscall]"]['dec0'].values[0]
    rsyslog = rsyslog[rsyslog.address < vsyscall]

    max_range = len(str(rsyslog['address'].max()))+1
    min_range = len(str(rsyslog['address'].min()))-1
    biny = [pow(10, x)  for x in range(min_range, max_range)]
    rsyslog['labely'] = pd.cut(x=rsyslog['address'], bins=biny) 
     

    # subyranges = [ [group.address.min(), group.address.max()] for name, group in rsyslog.groupby('labely') ]

    subyranges = [[int(x) for x in joined.loc[joined['pathname'].str.contains('hugeheap2')]['dec0']]] 


    fig = plt.figure()
    axes = plt.subplot(111)
    #axes.set_yticks(subyranges)
    #axes.set_yticklabels(('heaphuge2[0]', 'heaphuge2[536870911]'), rotation='vertical')
    
    print "$ add data to plots"
        
    #for idx in range(len(subxranges)-1,-1,-1):
    for idy in range(0, len(subyranges)):
        #plt.subplots_adjust(hspace =0.2)
        converty = len(subyranges)-(idy+1)
    
    #axes[idy][idx].set_xlim(subxranges[idx][0], subxranges[idx][1])
        axes.set_ylim(subyranges[converty][0] - 10, subyranges[converty][1]+10)
        axes.plot(rsyslog.timestamp, rsyslog.address, label=labels['fault'], c=colors['fault'], marker='o', linestyle=' ', ms=5, zorder=zorders['fault'])
        #axes[idy].set_ylim(subyranges[converty][0], subyranges[converty][1])
        #axes[idy].plot(rsyslog.timestamp, rsyslog.address, label=labels['fault'], c=colors['fault'], marker='o', linestyle=' ', ms=5, zorder=zorders['fault'])
        #for key, row in joined[joined['pathname'].str.contains('hugeheap2')].iterrows():
         #   axes[idy].axhline(y=row['dec0'], color='r', linestyle=':', lw=2)
        
                        
    plt.legend()
    plt.suptitle('Virtal Address by timeline')
    plt.xlabel('timestamp')
    plt.ylabel('Virtal Address')


    # output
    print "$ save plot"
    plt.savefig(dir_path+"/plot.png",format='png')
    if os.environ.get('DISPLAY','') != '':
     	plt.show()

plot_out('.', 0)
