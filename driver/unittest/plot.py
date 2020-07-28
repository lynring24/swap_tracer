import os
import sys
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



def plot_out():
    print "$ generate plot png"

    fig, axis = plt.subplots()

    swap_trace = pd.read_csv(sys.argv[1])
    swap_trace['timestamp'] = swap_trace.index
    #swap_trace = swap_trace[swap_trace['cmd']=='linear']
   
    groups = swap_trace.groupby('mode')
    #groups = swap_trace[swap_trace['mode']!='map'].groupby('mode')
    # out = swap_trace[swap_trace['mode']=='out']

    # add allocation trace if needed
    # add rsyslogs to plot 
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O'}
    colors={'in':'red', 'out':'blue', 'map':'green', 'writepage':'green'}

    for name, group in groups:
	if name =='out':
		axis.plot(group.timestamp, group.swpentry, label=labels[name], color=colors[name], marker='o', linestyle='', ms=5)
        # axis.plot(group.timestamp, group.address, label=labels[name], color=colors[name], marker='o', linestyle='', ms=5)
        # axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=5)


    #axis.plot(swap_trace.index, swap_trace.swpentry, label='swap cache #', color='blue', marker='o', linestyle='', ms=5)

    
    # axis.annotate(summary_str, xy=(0.5, 0), xycoords=('axes fraction', 'figure fraction'), xytext=(0, 10), textcoords='offset points', size=14, ha='center', va='bottom')

    axis.legend()
    # plt.text(6, 15, summary_str)

    axis.grid(True)
    axis.set_title('Swap Out pattern by timeline')
    #axis.set_title('VPN  access pattern by timeline')
    axis.set_xlabel('timestamp')
    axis.set_ylabel('Swap Cache Entry')
    axis.set_xscale('linear')
    axis.set_yscale('linear')


    # output
    plt.savefig("./plot.png",format='png')
    plt.show()


track_allocation=False
plot_out()
