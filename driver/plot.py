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

    fig, axis = plt.subplots()

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    # TODO : Expand to Nanosecond Timestamp
    rsyslog['timestamp'] = rsyslog.index
    # TODO : Exclude not child thread infos  

    # groups = rsyslog[rsyslog['mode']!='map'].groupby('mode')
    groups = rsyslog.groupby('mode')

    summary_str = "\n[Summary]\n"
    # add allocation trace if needed

    # add rsyslogs to plot 
    modes = ['fault', 'map', 'out']
    labels={'in':'swap-in','map':'memory map', 'fault':'page fault','out':'swap-out', 'writepage':'file I/O'}
    colors={'in':'red', 'out':'blue', 'map':'green', 'fault':'purple', 'allocation':'pink' }
    zorders={'fault':10, 'map':5, 'out':0}

    for name, group in groups:
	if name in modes:
		axis.plot(group.timestamp, group.address, label=labels[name], c=colors[name], marker='o', linestyle='', ms=5, zorder=zorders[name])
		summary_str = summary_str + "\n * memory {} # : {}".format(labels[name], len(group.index)) 
    summary_str = summary_str + "\n * average existence time in memory (usec) : {}".format(mean_time)


    axis.legend()
    plt.text(0.05, pow(10, 6), summary_str)

    axis.grid(True)
    axis.set_title('Virtual Page Number by timeline')
    axis.set_xlabel('timestamp')
    axis.set_ylabel('Virtual Page Number')

    # output
    plt.savefig(dir_path+"/plot.png",format='png')
    if os.environ.get('DISPLAY','') != '':
    	plt.show()

