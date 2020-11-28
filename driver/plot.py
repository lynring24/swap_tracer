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
PADDING = pow(10,3)

SEC_TO_USEC = 1000000

def plot_out(dir_path, option):            
    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    if len(rsyslog) < 2: 
        print "[Debug] swap not occured"
        exit(1)

    rsyslog['gap'] = rsyslog['address'].diff()
    rsyslog.to_csv(dir_path+"/gap.csv")

    print "calculate range"
    #rsyslog['timestamp'] = rsyslog['timestamp'].astype(int).apply(lambda x:x/SEC_TO_USEC)
    START_ADDRESS = rsyslog.address.min()-PADDING
    START_DIGITS = len(str(START_ADDRESS))-1
    #STEP = 0.001*pow(10,START_DIGITS)
    STEP = pow(10,START_DIGITS)
    END_ADDRESS = rsyslog.address.max()+PADDING

    subyranges = [ n for n in np.arange( START_ADDRESS, END_ADDRESS, STEP)] 
    subyranges.extend([1.8*pow(10,19), 1.9*pow(10,19)])

    rsyslog['axis'] = pd.cut(rsyslog['address'], bins=subyranges) 
    GRIDS = rsyslog['axis'].nunique()
    
    def add_weight(x):
        weighted = None
        if x > 0.3 :
            weighted = int(x*80)
        elif x > 0.1:
            weighted = int(x*150)
        else: 
            weighted = 4
        return weighted


    print "add range"
    height_ratios = map(lambda x : add_weight(x), rsyslog['axis'].value_counts(normalize=True).loc[lambda x: x > 0].sort_index(ascending=False).tolist())

    #print height_ratios

    print "\n$ generate plot [ {} x 1 ] ".format(GRIDS)

    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, gridspec_kw={'height_ratios':height_ratios}, sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    
    axes = axes.flatten() if GRIDS > 1 else [axes]

    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    
    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    colors = {'out' : 'red', 'map' : 'green'} 

    idy = -1  
    
    print "$ building plot"
    
    for name, region in rsyslog.groupby("axis"):
        if len(region) < 1:
            continue
        idy = idy+1
        converty = GRIDS-(idy+1)
        for mode, group in region.groupby('mode'):
            axes[converty].plot(group.timestamp, group.address, label=labels[mode], c=colors[mode], marker='o', linestyle=' ', ms=1, zorder=zorders[mode])

        REGION_START = min(region['address'])
        REGION_END =  max(region['address'])
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

        ticks = None
        if height_ratios[converty] > 50:
           ticks = map(lambda x: x.left, region['address'].value_counts(bins=3).sort_index().index.tolist())
           ticks.append(REGION_END)
        elif height_ratios[converty] > 20:
           ticks = map(lambda x: x.left, region['address'].value_counts(bins=2).sort_index().index.tolist())
           ticks.append(REGION_END)
        else:
            #ticks = [REGION_START, REGION_END]
            ticks = []
        axes[converty].set_yticks(ticks)



    
    patches = None 
    patches = [mpatches.Patch(color = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in colors.iteritems()]

    legend = axes[0].legend(handles = patches, bbox_to_anchor=(1.05, 1))
    plt.suptitle('Swap Trace [Address x timestamp]',fontsize=10)
    fig.text(0.5, 0.04, 'timestamp (sec) ', ha='center')
    fig.text(0.05, 0.5, 'Virtual Address', va='center', rotation='vertical')
    textstr = 'Mem.used(MiB):{}\n@: [{}, {}]\ntime(sec):{}'.format(END_ADDRESS-START_ADDRESS, hex(START_ADDRESS), hex(END_ADDRESS), (rsyslog.timestamp.max() - rsyslog.timestamp.min())/SEC_TO_USEC)
    fig.text(1.5, 0.05, textstr)
    plt.savefig("{}/result.png".format(dir_path),bbox_extra_artists=(legend,),bbox_inches='tight', format='png', dip=100)

    if os.environ.get('DISPLAY','') != '':
        plt.show()

if __name__ == "__main__":
    print "enter"
    if len (sys.argv) < 2: 
        plot_out(os.getcwd(), "mode")
    else:
        print "Usage : python plot.py"
    
    print "\n[Finish]"
