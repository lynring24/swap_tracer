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
    fig, axis = plt.subplots()
    groups = csvfile.groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault', 'writepage':'file I/O', 'alloc':'allocation'}
    for name, group in groups:
        axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)
    #ax.legend(numpoints=1)
    axis.legend(loc='best')
    axis.grid(True)
    axis.set_title('time - virtual page number')
    axis.set_xlabel('timestamp (usec)')
    axis.set_ylabel('virtual page number')
    axis.set_xscale('log')
    axis.set_yscale('log')

    # output
    plt.savefig(mergecsv[:-9]+'scatter.png',format='png')
    # plt.show()

