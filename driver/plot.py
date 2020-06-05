import os
import pandas as pd
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

def draw_png(mergecsv):
    print "$ generate plot png"

    csvfile = pd.read_csv(mergecsv)
    labels = csvfile['mode'].unique() 
    fig, ax = plt.subplots()
    groups = csvfile.groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O', 'alloc':'allocation'}
    for name, group in groups:
        ax.plot(group.timestamp, group.address, label=labels[name], marker='o', linestyle='', ms=2)
    #ax.legend(numpoints=1)
    ax.legend(loc='best')
    ax.grid(True)
    plt.xlabel('timestamp (usec)')
    plt.ylabel('virtual page number')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig(mergecsv[:-9]+'vpn.png',format='png')
    # print swpentry plot
    for name, group in groups:
        ax.plot(group.timestamp, group.address, label=labels[name], marker='o', linestyle='', ms=2)

    # plt.show()
