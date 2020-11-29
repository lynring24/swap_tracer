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
    #rsyslog['gap'] = rsyslog['address'].diff()
    #rsyslog.to_csv(dir_path+"/gap.csv")

    maps=pd.read_csv(dir_path+"/maps", sep='\s+',header=None, usecols=[0,5])
    maps.columns = ['range', 'pathname']
    #maps['range'] = maps['range'].apply(lambda x : map(lambda i : int(i,16), x.split('-')))
    maps = maps.join(maps['range'].str.split('-', expand=True).add_prefix('range')) 
    maps['range0'] = maps['range0'].apply(lambda x: int(x,16))
    maps['range1'] = maps['range1'].apply(lambda x: int(x,16))
    maps['gap'] = maps['range0'].diff()
    maps.to_csv(dir_path+"/gap.csv")

    #print maps.nlargest(4, 'gap')

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    if len(rsyslog) < 2: 
        print "[Debug] swap not occured"
        exit(1)

    rsyslog = rsyslog.sort_values('address', ascending =0)
    rsyslog['prev'] = rsyslog['address'].shift(1)
    rsyslog['gap'] = rsyslog['address'].diff()
    rsyslog = rsyslog.sort_values('gap')
    #print rsyslog.head(5)
    rsyslog.to_csv('sorted.csv')
    #print  rsyslog.nsmallest(4,'gap')
    
    ADDRESS_RANGE = [rsyslog.address.min()-1, rsyslog.address.max()+1]
    limits = ADDRESS_RANGE

    for index, row in rsyslog[rsyslog['gap'] < -1 * pow(10,10)].nsmallest(3,'gap').iterrows():
        print row['address'], row['prev'] , row['gap']
        # pandas cut the category by ( , ] so the addresws +1 , prev-1
        limits.extend([row['address']+1, row['prev']-1])

    limits = sorted(limits)



    print "calculate range"
    #START_ADDRESS = rsyslog.address.min()-PADDING
    #START_DIGITS = len(str(START_ADDRESS))-1
    #STEP = 0.001*pow(10,START_DIGITS)
    #STEP = pow(10,START_DIGITS)
    #END_ADDRESS = rsyslog.address.max()+PADDING
    
    SECONDS = True
    if rsyslog.timestamp.max() < (SEC_TO_USEC * 60) :
        rsyslog['timestamp'] = rsyslog['timestamp'].astype(int).apply(lambda x:x*SEC_TO_USEC)
        SECONDS = False



    #subyranges = [ n for n in np.arange( START_ADDRESS, END_ADDRESS, STEP)] 
    #subyranges.extend([1.8*pow(10,19), 1.9*pow(10,19)])

    rsyslog['axis'] = pd.cut(rsyslog['address'], bins=limits) 
    GRIDS = len(zip( limits[::2], limits[1::2]))
    
    def add_weight(x):
        weighted = None
        if x > 0.3 :
            weighted = int(x*70)
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
    fig.text(0.05, 0.5, 'Virtual Address', va='center', rotation='vertical')

    textstr = None
    if SECONDS == True:
        fig.text(0.5, 0.04, 'timestamp (sec) ', ha='center')
        textstr = 'Mem.used @: [{}, {}]\ntime(sec):{}'.format(hex(ADDRESS_RANGE[0]), hex(ADDRESS_RANGE[1]), (rsyslog.timestamp.max() - rsyslog.timestamp.min()))
    else:
        fig.text(0.5, 0.04, 'timestamp (usec) ', ha='center')
        textstr = 'Mem.used @: [{}, {}]\ntime(sec):{}'.format(hex(ADDRESS_RANGE[0]), hex(ADDRESS_RANGE[1]), (rsyslog.timestamp.max() - rsyslog.timestamp.min())/SEC_TO_USEC)

    fig.text(0.6, 0.5, textstr)
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
