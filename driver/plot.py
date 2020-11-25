import os
import sys
import pandas as pd
import numpy as np
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from datetime import datetime, timedelta

labels={'map':'swap-in','fault':'page fault','out':'swap-out', 'writepage':'file I/O', 'handle_mm':'total page fault', 'create':'allocation'}
zorders={'fault':5, 'map':10, 'out':0}
markers = { 'map':'o', 'out':'x', 'fault' :'^'}
 
PADDING = 5*pow(10,5)

SEC_TO_USEC = 100000

def plot_out(dir_path, option):            
    MODE = "mode"
    MMAP = "mmap"
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None, usecols=[0,5])
    maps.columns = ['range','pathname']   
    maps['pathname'] = maps['pathname'].fillna('Anon') 
    maps = maps.join(maps['range'].str.split('-', expand=True).add_prefix('range'))
    maps['range0'] = maps['range0'].apply(lambda x: int(x, 16))
    maps['range1'] = maps['range1'].apply(lambda x: int(x, 16))
    maps = maps.drop('range', axis=1)
    maps['merge'] = ((maps['range0'].shift(-1) == maps['range1'])  & (maps['pathname'].shift(-1)==maps['pathname'])) | ((maps['range1'].shift() == maps['range0']) & (maps['pathname'].shift()==maps['pathname']))

    for name, group in maps[maps['merge']==True].groupby('pathname'):
        head = group.range0.min()
        tail = group.range1.max()
        #print head, tail
        new_row = {'pathname':name, 'range0':head, 'range1':tail, 'merge':False}
        maps = maps.append(new_row, ignore_index=True)
    maps = maps[maps['merge']==False].sort_values('range0', ascending=1)

    def shorted(x):
        if os.path.isabs(x):
           return os.path.basename(x).split('.')[0]
        else:
           if '[' in x: 
                x=x.replace('[','')
                x=x.replace(']','')
           return x
    maps['pathname'] = maps['pathname'].apply(lambda value : shorted(value))
    maps = maps.reset_index()


    # find biggest gap 
    #maps['gap'] = maps['range0'].shift(-1) - maps['range1']
    #maps['next_start'] = maps['range0'].shift(-1)
    maps = maps[['range0', 'range1', 'pathname']]

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    if len(rsyslog) < 2: 
        print "[Debug] swap not occured"
        exit(1)

    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int).apply(lambda x:x/SEC_TO_USEC)
    keys = list( zip(maps.range0, maps.range1)) 
    layout = pd.Series(maps.pathname.values, index=keys).to_dict()

    def labelize(x):
        diff = None
        label = None 
        for key in sorted(layout):
            if key[0] <= x and  x <= key[1]: 
                return layout[key]
            ## x value is bigger than the segment 
            elif key[1] <= x: 
                diff = abs(x - key[1])
                label = layout[key]
            else: 
                if diff >= abs(x - key[0]):
                    label= layout[key]
                break
        return label 

    rsyslog['address'] = rsyslog['address'].apply(lambda x: x)
    rsyslog['mmap'] = rsyslog['address'].apply(lambda x : labelize(x))

    del maps

    # output

    START_ADDRESS = rsyslog.address.min()-PADDING
    START_DIGITS = len(str(START_ADDRESS))
    print rsyslog.address.min(), rsyslog.address.max()
    STEP = 0.001*pow(10,START_DIGITS)
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


    height_ratios = map(lambda x : add_weight(x), rsyslog['axis'].value_counts(normalize=True).loc[lambda x: x > 0].sort_index(ascending=False).tolist())

    #print height_ratios

    print "\n$ generate plot [ {} x 1 ] by {}".format(GRIDS, option)

    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, gridspec_kw={'height_ratios':height_ratios}, sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    
    axes = axes.flatten() if GRIDS > 1 else [axes]

    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    
    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    colors=dict()
    if option == MMAP:
        color_list = list(mcolors.TABLEAU_COLORS)
        def paint(mmap):
            colors.update({mmap : color_list.pop(-1)})
        map( lambda x:paint(x), rsyslog.mmap.unique().tolist())
    else:
        colors = {'out' : 'red', 'map' : 'green'} 

    idy = -1  
    for name, region in rsyslog.groupby("axis"):
        if len(region) < 1:
            continue
        idy = idy+1
        converty = GRIDS-(idy+1)
        for (area, mode), group in region.groupby(['mmap', 'mode']):
            if option==MMAP:
                axes[converty].plot(group.timestamp, group.address, label=labels[mode], c=colors[area], marker=markers[mode], linestyle=' ', ms=1, zorder=zorders[mode])
            else:
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
            ticks = [REGION_START, REGION_END]
        axes[converty].set_yticks(ticks)



    
    patches = None 
    if option == MMAP :
        patches = [mpatches.Patch(color = value, label = '{} ({})'.format(key, len(rsyslog[rsyslog['mmap'] == key]))) for key, value in colors.iteritems()]
        patches.extend([mpatches.Patch(hatch = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in markers.iteritems()])
    else:
        patches = [mpatches.Patch(color = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in colors.iteritems()]

    legend = axes[0].legend(handles = patches, bbox_to_anchor=(1.05, 1))
    plt.suptitle('Swap Trace [Address x timestamp]',fontsize=10)
    fig.text(0.5, 0.04, 'timestamp (sec) ', ha='center')
    fig.text(0.05, 0.5, 'Virtual Address', va='center', rotation='vertical')
    textstr = 'Mem.used(MiB):{}\n@: [{}, {}]\ntime(sec):{}'.format(END_ADDRESS-START_ADDRESS, hex(START_ADDRESS), hex(END_ADDRESS), (rsyslog.timestamp.max() - rsyslog.timestamp.min())/SEC_TO_USEC)
    fig.text(1.75, 0, textstr)
    plt.savefig("{}/result.png".format(dir_path),bbox_extra_artists=(legend,),bbox_inches='tight', format='png', dip=100)

    if os.environ.get('DISPLAY','') != '':
        plt.show()

if __name__ == "__main__":
    if len (sys.argv) < 2: 
        plot_out(os.getcwd(), "mode")
    elif sys.argv[1] == '--mmap' or sys.argv[1] == '-m':
        plot_out(os.getcwd(), "mmap")
    else:
        print "Usage : python plot.py <--mmap | -m>"
    
    print "\n[Finish]"
