import os
import pandas as pd
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


class Tracker(object):
    def __init__(self, axis, data):
        self.axis = axis
        self.data = data

    def add_plot(self, row): 
        x = [row[0], row[0]]
        y = [row[1], row[2]]
        self.axis.plot(x, y, linestyle='dashed', markersize=12)

    def run(self):
        pool = Pool(processes=cpu_count())
        return pool.map(self.add_plot, self.data)



def plot_out(dir_path, mean_time):
    print "$ generate plot png"


    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog = rsylog.query('cmd=="linear"')
    max_range = len(str(rsyslog['timestamp'].max()))
    bins = [pow(10, x) for x in range(0, max_range)]
    rsyslog['label'] = pd.cut(x=rsyslog['timestamp'], bins=bins)
  
    mode = 'out'
    summary_str = "\n[Summary]\n"
    labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O'}
    colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'pink' }
    zorders={'fault':5, 'map':10, 'out':0}
    
    subranges=[]
    for name, group in rsyslog.groupby('label'):
        if (group.index) > 0:
            subranges.append([group.timestamp.min(), group.timestamp.max()])
            
    fig, axes = plt.subplots(ncols=len(subranges), nrows=1, sharey=True)

    ax = .plot(group.timestamp, group.address, label=labels[mode], c=colors[mode], marker='o', linestyle='', ms=5, zorder=zorders[mode])
    summary_str = summary_str + "\n * memory {} # : {}".format(labels[mode], len(group.index)) 

    axis.legend()
    plt.text(0.05, pow(10, 6), summary_str)

    axis.grid(True)
    axis.set_title('Virtal Address by timeline')
    axis.set_xlabel('timestamp')
    axis.set_ylabel('Virtal Address')

    # output
    plt.savefig(dir_path+"/plot.png",format='png')
    if os.environ.get('DISPLAY','') != '':
    	plt.show()


plot_out('.', 0)
