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

MICROSECOND = 1000000


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
    COUNT_BREAKS = 4
    break_points = maps.sort_values(['gap'],ascending=[0]).head(COUNT_BREAKS)
    break_points = break_points.sort_values('range0', ascending=1)[['range1', 'next_start']].to_numpy().tolist()
    maps = maps[['range0', 'range1', 'pathname']]

    rsyslog = pd.read_csv(dir_path+"/rsyslog.csv")
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

    digits = len(str(rsyslog['address'].min()))-1
    START_OF_ADDRESS = maps.range0.min()
    END_OF_ADDRESS = maps.range1.max() 

    subyranges = [[START_OF_ADDRESS, break_points[0][0]]]

    for idx in range(1, COUNT_BREAKS):
       HEAD = None
       TAIL = None
       if idx < COUNT_BREAKS - 1 :
          HEAD = break_points[idx][1]
          TAIL = break_points[idx+1][0]
       else:
          HEAD = break_points[idx][0]
          TAIL = END_OF_ADDRESS 

       if len(rsyslog[(HEAD <= rsyslog['address']) & (rsyslog['address'] <= TAIL)]) > 0:
          subyranges.append([HEAD, TAIL]) 

    GRIDS = len(subyranges) 
    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)
    
    axes = axes.flatten()

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
    
    for idy in range(0, GRIDS):
        for (area, mode), group in rsyslog.groupby(['label', 'mode']):
            if option==AREA:
                axes[idy].plot(group.timestamp, group.address, label=labels[mode], c=colors[area], marker=markers[mode], linestyle=' ', ms=1, zorder=zorders[mode])
            else:
                axes[idy].plot(group.timestamp, group.address, label=labels[mode], c=colors[mode], marker='o', linestyle=' ', ms=1, zorder=zorders[mode])

        converty = GRIDS-(idy+1)
        axes[idy].set_ylim(subyranges[converty][0]-PADDING, subyranges[converty][1]+PADDING)

        if idy == 0:
            axes[idy].spines['top'].set_visible(True)

        if idy == GRIDS-1:
            axes[idy].spines['bottom'].set_visible(True)

        if idy == 0:
            axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
        else:
            kwargs.update(transform=axes[idy].transAxes)  # switch to the bottom axes
            axes[idy].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
            axes[idy].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
            axes[idy].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
            axes[idy].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal             
    
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

# plot_out('.', MODE)
