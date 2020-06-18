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
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    groups = csvfile.groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O', 'alloc':'allocation'}
    for name, group in groups:
        ax1.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)
    #ax.legend(numpoints=1)
    ax1.legend(loc='best')
    ax1.grid(True)
    ax1.set_title('time - virtual page number')
    ax1.set_xlabel('timestamp (usec)')
    ax1.set_ylabel('virtual page number')
    ax1.set_xscale('log')
    ax1.set_yscale('log')

    # print swpentry plot
    for name, group in groups:
        if name != 'writepage':
            ax2.plot(group.timestamp.astype(str), group.swpentry.astype(str), label=labels[name], linestyle='', ms=2)
    ax2.legend(loc='best')
    ax2.grid(True)
    # ax2.set_title('time - swap cache entry ')
    ax2.set_xlabel('timestamp (usec)')
    ax2.set_ylabel('swap chace entry')

    ax2.set_xscale('log')
    ax2.set_yscale('log')

    # output
    plt.savefig(mergecsv[:-9]+'scatter.png',format='png')
    # plt.show()

