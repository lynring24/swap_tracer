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



def plot_out(dir_path, track_allocation=False):
    print "$ generate plot png"

    swap_trace = pd.read_csv(dir_path+"/merge.csv")
    labels = swap_trace['mode'].unique() 
    fig, axis = plt.subplots()
    groups = swap_trace[swap_trace['mode']!='map'].groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O'}
    for name, group in groups:
        axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)

    # add allocation trace if needed
    if track_allocation:
        print "$ generate allocation trace"
        allocations=pd.read_csv(dir_path+"/hook.csv")
        tracker = Tracker(axis, allocations[['timestamp','address' ,'end']].values.tolist())
        tracker.run()

    #ax.legend(numpoints=1)
    axis.legend(loc='best')
    axis.grid(True)
    axis.set_title('time - virtual page number')
    axis.set_xlabel('timestamp (usec)')
    axis.set_ylabel('virtual page number')
    axis.set_xscale('log')
    axis.set_yscale('log')

    # output
    plt.savefig(dir_path+"/plot.png",format='png')
    # plt.show()

