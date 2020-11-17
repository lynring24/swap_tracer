import os
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
MODE = "mode"
AREA = "area"

def plot_out(dir_path, option):            
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None, usecols=[0,5])
    maps.columns = ['range','pathname']   
    maps['pathname'] = maps['pathname'].fillna('Anon') 
    maps = maps.join(maps['range'].str.split('-', expand=True).add_prefix('range'))
    maps['range0'] = maps['range0'].apply(lambda x: int(x, 16))
    maps['range1'] = maps['range1'].apply(lambda x: int(x, 16))
    maps = maps.drop('range', axis=1)
    maps['merge'] = (maps['pathname'].shift(-1) == '[Anon]') & (maps['range0'].shift(-1) == maps['range1']) & (maps['pathname'].str.contains('/lib/')==False)

    indexs = maps[maps['merge'] == True].index
    for index in indexs:
        under = index+1 
        if maps.iloc[under]['merge'] == False:
            maps.at[index, 'range1'] = maps.iloc[under]['range1']
            maps = maps.drop(under) 

    def shorted(x):
        if os.path.isabs(x):
           return os.path.basename(x).split('.')[0]
        else:
           if '[' in x: 
                x=x.replace('[','')
                x=x.replace(']','')
           return x
    ## pathname 
    maps['pathname'] = maps['pathname'].apply(lambda value : shorted(value))
    maps = maps.reset_index()

    # find biggest gap 
    maps['gap'] = maps['range0'].shift(-1) - maps['range1']
    maps['next_start'] = maps['range0'].shift(-1)
    maps = maps[['range0', 'range1', 'pathname']]

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
    if len(rsyslog) < 2: 
        print "[Debug] swap not occured"
        exit(1)

    rsyslog['timestamp'] = rsyslog['timestamp'].astype(int)
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

    rsyslog['label'] = rsyslog['address'].apply(lambda x : labelize(x))
    rsyslog.to_csv('./labelized.csv')

    # output
    print "\n$ plot by {}".format(option)

    START_OF_ADDRESS = rsyslog.address.min()
    END_OF_ADDRESS = rsyslog.address.max() 

    #biny = [START_OF_ADDRESS, 1.0*pow(10, 14), 1.3*pow(10,14), 1.4*pow(10,14), END_OF_ADDRESS , 1.8 *pow(10, 18) ]
    #biny = [ n*pow(10, 14) for n in np.arange(1,3 , 0.1) ]
    #biny = [ pow(10, n) for n in range(14, 20) ]
    # biny.extend([START_OF_ADDRESS, END_OF_ADDRESS])

    mmap = rsyslog.groupby('label')['address'].agg([('start' , 'min'), ('end', 'max')]).sort_values('start', ascending=1) 
    COUNT_BREAKS = 2 
    mmap['next'] = mmap['start'].shift(-1)   
    mmap['rear'] = mmap['next']-mmap['end']

    break_points = mmap.sort_values('rear', ascending=0).head(2)
    break_points = break_points.sort_values('start', ascending=1)[['end', 'next']].to_numpy().tolist()
    biny = sum(break_points, [])
    biny.extend([START_OF_ADDRESS, END_OF_ADDRESS])
    biny = sorted(biny)
    subyranges = zip(biny[::2], biny[1::2])

    def mmap(x):
        for region in subyranges:
            if region[0]<=x and x <= region[1]:
                return region
    rsyslog['axis'] = rsyslog['address'].apply(lambda x : mmap(x))
    
    GRIDS = len(subyranges)

    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    
    axes = axes.flatten() if GRIDS > 1 else [axes]

    # set spines false
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    
    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    colors=dict()
    if option == AREA:
        def set_color_list():
            return list(mcolors.TABLEAU_COLORS)
        color_list = set_color_list()
        def paint(label):
            colors.update({label : color_list.pop(-1)})
        map( lambda x:paint(x), rsyslog.label.unique().tolist())
    else:
        colors = {'out' : 'red', 'map' : 'green'} 

    idy = -1  
    for name, region in rsyslog.groupby("axis"):
        if len(region) < 1:
            continue
        idy = idy+1
        converty = GRIDS-(idy+1)
        for (area, mode), group in region.groupby(['label', 'mode']):
            if option==AREA:
                axes[converty].plot(group.timestamp, group.address, label=labels[mode], c=colors[area], marker=markers[mode], linestyle=' ', ms=1, zorder=zorders[mode])
            else:
                axes[converty].plot(group.timestamp, group.address, label=labels[mode], c=colors[mode], marker='o', linestyle=' ', ms=1, zorder=zorders[mode])


        axes[converty].set_ylim(min(region['address'])-PADDING, max(region['address'])+PADDING)


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
    
    patches = None 
    if option == AREA :
        patches = [mpatches.Patch(color = value, label = '{} ({})'.format(key, len(rsyslog[rsyslog['label'] == key]))) for key, value in colors.iteritems()]
        patches.extend([mpatches.Patch(hatch = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in markers.iteritems()])
    else:
        patches = [mpatches.Patch(color = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in colors.iteritems()]

    legend = axes[0].legend(handles = patches, bbox_to_anchor=(1.05, 1))
    plt.savefig("{}/result.png".format(dir_path),bbox_extra_artists=(legend,),bbox_inches='tight', format='png', dip=100)

    if os.environ.get('DISPLAY','') != '':
        plt.show()

if __name__ == "__main__":
    plot_out('.', AREA)
