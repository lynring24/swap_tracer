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



def plot_out(dir_path, mean_time, command):
    print "$ generate plot png"


    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    rsyslog = rsyslog.query('cmd=="{}"'.format(command))
    max_range = len(str(rsyslog['timestamp'].max()))
    bins = [pow(10, x) for x in range(0, max_range)]
    rsyslog['label'] = pd.cut(x=rsyslog['timestamp'], bins=bins)
  
    summary_str = "\n[Summary]\n"
    labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault'}
    colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'pink', 'handle_mm':'pink' }
    zorders={'fault':5, 'map':10, 'out':0, 'handle_mm':3}
    
    subranges=[]
    idx  =0 
    for name, group in rsyslog.groupby('label'):
        if (len(group.index)) > 0:
            subranges.append([max(group.timestamp.min(), 0)  , group.timestamp.max() + 10])
            idx = idx +1
            
    fig, axes = plt.subplots(ncols=len(subranges), nrows=1, sharey=True)
    fig.tight_layout()

    total_axes = len(axes) 

    print total_axes, idx

    for idx in range(0, total_axes):
        plt.subplots_adjust(hspace =0.2)
        axes[idx].set_xlim(subranges[idx][0], subranges[idx][1])
        #if idx == 0: 
        #    axes[idx].spines['right'].set_visible(False)
        #elif idx == total_axes-1:
        #    axes[idx].spines['left'].set_visible(False)
        #else:
        #    axes[idx].spines['left'].set_visible(False)
        #    axes[idx].spines['right'].set_visible(False)
        for name, group in rsyslog.groupby('mode'):
            axes[idx].plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle=' ', ms=5, zorder=zorders[name])

    summary = "\n [Summary] \n"
    for name, group in rsyslog.groupby('mode'):
        summary = summary + "\n memory {} # : {}".format(labels[name], len(group.index))
    summary = summary + "\n * average existense time in memory (usec) : {}".format(mean_time)


    plt.text(0.05, pow(10, 5), summary)
    axes[int(total_axes/2)].set_title('Virtal Address by timeline')
    axes[int(total_axes/2)].set_xlabel('timestamp')
    axes[0].set_ylabel('Virtal Address')


    # output
    plt.savefig(dir_path+"/plot.png",format='png')
    if os.environ.get('DISPLAY','') != '':
    	plt.show()
