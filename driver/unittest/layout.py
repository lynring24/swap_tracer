import os
import pandas as pd
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'allocation':'allocation'}
colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'brown', 'handle_mm':'magenta' }
zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}


def plot_out(dir_path, mean_time):
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None)
    maps.columns = ['layout', 'perm' , 'offset', 'duration', 'inode', 'pathname']
    maps['pathname'] = maps['pathname'].fillna('anon')
    
    maps = maps.join(maps['layout'].str.split('-', expand=True).add_prefix('layout'))
    maps = maps.drop('layout',1)

    layout = dict()
    for name, group in maps.groupby('pathname'):
        if name == 'anon':
           layout[name]=[]
           for index, row in group.iterrows():
                layout[name].append([row['layout0'], row['layout1']]) 
        else:
            head = group.layout0.min()
            tail = group.layout1.max()
            layout[name] = [head, tail]

    nsegment = sum(len(v) for v in layout.itervalues())
    fig, axes = plt.subplots(ncols=1, nrows=nsegments)

   # fig.tight_layout()
    



        
   # plt.legend()
   # plt.suptitle('Virtal Address by timeline')
 #   plt.xlabel('timestamp')
 #   plt.ylabel('Virtal Address')


    # output
  #  plt.savefig(dir_path+"/plot.png",format='png')
 #   if os.environ.get('DISPLAY','') != '':
  #   	plt.show()

plot_out('.', 0)
