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



def plot_out(dir_path, mean_time, track_allocation=False):
    print "$ generate plot png"

    fig, axis = plt.subplots()

    swap_trace = pd.read_csv(dir_path+"/merge.csv")
    groups = swap_trace[swap_trace['mode']!='map'].groupby('mode')

    summary_str = "\n[Summary]\n"

    # add allocation trace if needed
    if track_allocation:
        print "$ generate allocation trace"
        allocations=pd.read_csv(dir_path+"/hook.csv")
        tracker = Tracker(axis, allocations[['timestamp','address' ,'end']].values.tolist())
        tracker.run()
        summary_str = summary_str + "\n * memory allocation # :{}".format(len(allocations.index))

    # add rsyslogs to plot 
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O'}

    for name, group in groups:
        axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)
        summary_str = summary_str + "\n * memory {} # : {}".format(labels[name], len(group.index)) 
    summary_str = summary_str + "\n * average existence time in memory (usec) : {}".format(mean_time)

    # axis.annotate(summary_str, xy=(0.5, 0), xycoords=('axes fraction', 'figure fraction'), xytext=(0, 10), textcoords='offset points', size=14, ha='center', va='bottom')

    axis.legend()
    # plt.text(6, 15, summary_str)
    plt.text(6, 30, summary_str)

    axis.grid(True)
    axis.set_title('VPN by timeline')
    axis.set_xlabel('timestamp (usec)')
    axis.set_ylabel('virtual page number')
    axis.set_xscale('log')
    axis.set_yscale('log')

    # output
    plt.savefig(dir_path+"/plot.png",format='png')
    # plt.show()

