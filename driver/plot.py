import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

labels={'map':'swap-in','fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'create':'allocation'}
zorders={'fault':5, 'map':10, 'out':0}
markers = { 'map':'o', 'out':'x', 'fault' :'^'}
 
#PADDING = 5*pow(10,5)
PADDING = pow(10,5)

SEC_TO_USEC = 1000000

def plot_out(dir_path, option):            
    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    if len(rsyslog) < 2: 
        print "[Debug] swap not occured"
        exit(1)
    #rsyslog = rsyslog[rsyslog['mode'] == 'out']

    rsyslog = rsyslog.sort_values('address', ascending =0)
    rsyslog['prev'] = rsyslog['address'].shift(1)
    rsyslog['gap'] = rsyslog['address'].diff()
    rsyslog = rsyslog.sort_values('gap')
    #print rsyslog.head(5)
    #rsyslog.to_csv('sorted.csv')
    #print  rsyslog.nsmallest(4,'gap')
    
    ADDRESS_RANGE = [rsyslog.address.min()-1, rsyslog.address.max()+1]
    limits = ADDRESS_RANGE

    for index, row in rsyslog[rsyslog['gap'] < -1 * pow(10,10)].nsmallest(3,'gap').iterrows():
        limits.extend([row['address']+1, row['prev']-1])

    limits = sorted(limits)



    print " > sample range"

    rsyslog['axis'] = pd.cut(rsyslog['address'], bins=limits) 
    GRIDS = len(zip( limits[::2], limits[1::2]))
    
    def add_weight(x):
        weighted = None
        if x > 0.75 :
            weighted = int(x*50)
        elif x > 0.5 :
            weighted = int(x*75)
        elif x > 0.25:
            weighted = int(x*125)
        elif x > 0.1:
            weighted = int(x*150)
        else: 
            weighted = 5
        return weighted


    print " > add range"
    height_ratios = map(lambda x : add_weight(x), rsyslog['axis'].value_counts(normalize=True).loc[lambda x: x > 0].sort_index(ascending=False).tolist())

    #print height_ratios

    print " > generate plot [ {} x 1 ] ".format(GRIDS)

    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, gridspec_kw={'height_ratios':height_ratios}, sharex=True)
    #plt.subplots_adjust(wspace=0, hspace=0)
    plt.subplots_adjust(wspace=0, hspace=0.15)
    
    axes = axes.flatten() if GRIDS > 1 else [axes]

    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    
    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    colors = {'out' : 'red', 'map' : 'green'} 

    idy = -1  
    
    
    for name, region in rsyslog.groupby("axis"):
        if len(region) < 1:
            continue
        idy = idy+1
        converty = GRIDS-(idy+1)
        for mode, group in region.groupby('mode'):
            axes[converty].plot(group.timestamp, group.address, label=labels[mode], c=colors[mode], marker='o', linestyle=' ', ms=1, zorder=zorders[mode])

        REGION_START = min(region['address'])
        REGION_END =  max(region['address'])

        #LINE = 94029789184064
        #axes[converty].set_ylim(min(LINE, REGION_START-PADDING) , max(LINE, REGION_END+PADDING))
        axes[converty].set_ylim(REGION_START-PADDING, REGION_END+PADDING)

        if converty == 0:
            axes[converty].spines['top'].set_visible(True)

        if converty == GRIDS-1:
            axes[converty].spines['bottom'].set_visible(True)

        if converty != GRIDS-1:
            axes[converty].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[converty].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
        else:
            kwargs.update(transform=axes[converty].transAxes)  # switch to the bottom axes
            axes[converty].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
            axes[converty].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
            axes[converty].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[converty].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal           
        #TODO: set ticks 

        ticks = []
        if height_ratios[converty] > 50:
           ticks = map(lambda x: x.left, region['address'].value_counts(bins=3).sort_index().index.tolist())
           ticks.append(REGION_END)
           #ticks.extend([REGION_START, REGION_END])
        elif height_ratios[converty] > 20:
           ticks = map(lambda x: x.left, region['address'].value_counts(bins=2).sort_index().index.tolist())
           #ticks.extend([REGION_START, REGION_END])
           ticks.append(REGION_END)
        else:
            pass


        axes[converty].set_yticks(ticks)
        ticklabels = map(lambda x: format(int(x), 'x'), ticks)
        axes[converty].set_yticklabels(ticklabels, fontsize='7')
        #if converty == 0:
        #axes[converty].hlines(y=LINE, xmin=0, xmax=50, colors='red', linestyles='solid')


    
    patches = None 
    patches = [mpatches.Patch(color = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in colors.iteritems()]

    legend = axes[0].legend(handles = patches, bbox_to_anchor=(1.05, 1))
    plt.suptitle('Swap Trace [Address x timestamp]',fontsize=10)
    #fig.text(0.005,  0.5, 'Virtual Address', va='center', rotation='vertical')

    text_str  = 'virtual address : \n[{} ~ {}]\n'.format(format(int(ADDRESS_RANGE[0]), 'x'), format(int(ADDRESS_RANGE[1]), 'x'))
    #if SECONDS == True:
    fig.text(0.5, 0.04, 'timestamp (sec) ', ha='center')
    text_str = '{}\nexecution time (sec) : \n{}'.format(text_str, rsyslog.timestamp.max())
    #else:
    #    fig.text(0.5, 0.04, 'timestamp (usec) ', ha='center')
    #    text_str = '{}\ntime(sec) : {}'.format(text_str, (rsyslog.timestamp.max() - rsyslog.timestamp.min())/SEC_TO_USEC)

    fig.text(0.93, 0.5, text_str)
    plt.savefig("{}/result.png".format(dir_path),bbox_extra_artists=(legend,),bbox_inches='tight', format='png', dip=100)

    if os.environ.get('DISPLAY','') != '':
        plt.show()

if __name__ == "__main__":
    if len (sys.argv) < 2: 
        plot_out(os.getcwd(), "mode")
    else:
        print "Usage : python plot.py"
    
    print "\n[Finish]"
