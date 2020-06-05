import os
import pandas as pd
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt

def draw_png(mergecsv):
    csvfile = pd.read_csv(mergecsv)

    labels = csvfile['mode'].unique() 

    fig, ax = plt.subplots()

    groups = csvfile.groupby('mode')

    for name, group in groups:
        ax.plot(group.timestamp, group.address, label=name, marker='o', linestyle='', ms=10)
    #ax.legend(numpoints=1)
    ax.legend(loc='best')
    ax.grid(True)

    plt.xlabel('timestamp (usec)')
    plt.ylabel('virtual page number')
    plt.yscale('log')
    plt.savefig(mergecsv[:-9]+'scatter.png',format='png')
    # plt.show()
