import os
import pandas as pd
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy

def draw_png(mergecsv):
    print "$ Generate 6 Figures"

    csvfile = pd.read_csv(mergecsv)
    labels = csvfile['mode'].unique() 
    fig, axis = plt.subplots()
    # axes = list(numpy.concatenate(axes).flat)

    axis.legend(loc='best')
    axis.grid(True)
    axis.set_xscale('log')
    axis.set_yscale('log')
    

    groups = csvfile.groupby('mode')
    labels={'in':'swap-in', 'out':'swap-out', 'map':'page-fault','writepage':'file I/O', 'alloc':'allocation'}
    position = {'in': 2, 'out':3, 'map':1, 'writepage':4, 'dependancy':5}

    # fig 0 : print all in one 
    # print "$ Build Figure 0"
    # for name, group in groups:
    #   axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)   
    # plt.savefig('./{}.png'.format('total'),format='png')
    # plt.cla()
   
    # fig 1~4 : print each
    # print "$ Build Figure 1-4"
    # for name, group in groups:
     #   axis.plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)   
    #   plt.savefig('./{}.png'.format(name),format='png')
    #   plt.cla()
   
    # axes[position[name]].plot(group.timestamp.astype(str), group.address.astype(str), label=labels[name], marker='o', linestyle='', ms=2)

    # fig 5 : print tependancy
    related = pd.read_csv('./duplicated_address.csv')
    related = related.apply(pd.to_numeric)

    print "$ Build Figure 5"
    def plot_out(y, x1, x2):
        # axis.hlines(y=y, xmin=x1, xmax=x2)
        x = [x1, x2] 
        y = [y, y]
        axis.plot(x, y, linestyle='dashed', markersize=12)


    # related.apply(lambda row: plot_out([row['timestamp_x'], row['address']], [row['timestamp_y'], row['address']]), axis=1)
    related.apply(lambda row: plot_out(row['address'], row['timestamp_x'], row['timestamp_y']), axis=1)

    # output
    print "$ Save Figure"
    plt.title('swap in -> page out')
    plt.savefig('./{}.png'.format('linkage'),format='png')
    # plt.show()

draw_png('/home/hrchung/benchmarks/random/2020-07-01T16:42:56.977715/merge.csv')
