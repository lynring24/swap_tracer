import os
import pandas as pd
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy

def draw_png(mergecsv):
    print "$ generate plot png"

    csvfile = pd.read_csv(mergecsv)
    labels = csvfile['mode'].unique() 
    fig, axes = plt.subplots(nrows=3, ncols=2)
    axes = list(numpy.concatenate(axes).flat)

    for axis in axes:
        axis.legend(loc='best')
        axis.grid(True)
        axis.set_xscale('log')
        axis.set_yscale('log')

    groups = csvfile.groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault','writepage':'file I/O', 'alloc':'allocation'}
    position = {'in': 2, 'out':3, 'map':1, 'writepage':4, 'dependancy':5}

    # fig 0 : print all in one 
    print "$ Build Plots [0~4]"
    for name, group in groups:
        axes[0].plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)
        axes[position[name]].plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)

    # fig 5 : print tependancy
    related = pd.read_csv('./duplicated_address.csv')
    related = related.apply(pd.to_numeric)

    print "$ Build Plots [5]"
    #for index, row in related.iterrows():
    #    x1 = int(row['timestamp_x'])
    #    y = int(row['address'])
    #    x2 = int(row['timestamp_y'])
    # axes[5].plot([x1, y], [x2, y], 'k-')
    def plot_out(coor1, coor2):
        axes[5].plot(coor1, coor2, 'k-')
    related.apply(lambda row: plot_out([row['timestamp_x'], row['address']], [row['timestamp_y'], row['address']]), axis=1)

    # output
    # plt.savefig(mergecsv[:-9]+'scatter.png',format='png')
    print "$ Save Figure"
    plt.savefig('./scatter.png',format='png')
    # plt.show()

draw_png('/home/hrchung/benchmarks/random/2020-07-01T16:42:56.977715/merge.csv')
