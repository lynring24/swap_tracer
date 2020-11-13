import os
import pandas as pd
import numpy as np
import matplotlib as mpl
from multiprocess import Pool, cpu_count

if os.environ.get('DISPLAY','') == '':
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
def draw_landscape(dir_path):
            
    maps = pd.read_csv(dir_path+"/maps", sep='\s+',header=None, usecols=[0,5])
    maps.columns = ['range','pathname']   
    maps['pathname'] = maps['pathname'].fillna('Anon') 
    maps = maps.join(maps['range'].str.split('-', expand=True).add_prefix('range'))
    maps['range0'] = maps['range0'].apply(lambda x: int(x, 16))
    maps['range1'] = maps['range1'].apply(lambda x: int(x, 16))
    maps = maps.drop('range', axis=1)
    # merge heap, stack
    #maps['merge'] = (maps['pathname'].shift(-1) == '[Anon]') & (maps['range0'].shift(-1) == maps['range1']) & (maps['pathname'].str.contains('/lib/')==False)
    #indexs = maps[maps['merge'] == True].index
    #for index in indexs:
    #    under = index+1 
    #    if maps.iloc[under]['merge'] == False:
    #        maps.at[index, 'range1'] = maps.iloc[under]['range1']
    #        maps = maps.drop(under)    

    # fold map
    #maps['merge'] = (maps['range0'].shift(-1) == maps['range1']) & (maps['pathname'] == maps['pathname'].shift(-1)) 
  
    drops = []
    for name, group in maps.groupby('pathname'):
        # if the range is continuous 
        #group['merge'] = (group['range0'].shift(-1) == group['range1']) | (group['range1'].shift() == group['range0'])  
        group.loc[:, 'merge'] = (group['range0'].shift(-1) == group['range1']) | (group['range1'].shift() == group['range0'])  
        temp = group[group['merge']==True]
        if len(temp)> 1 :
            indexs = sorted(temp.index)
            addr = [temp['range0'].min(), temp['range1'].max()]
            #maps.set_value(indexs[0], 'range0', temp['range0'].min())
            #maps.set_value(indexs[0], 'range1', temp['range1'].max())
            AT = int(indexs[0])
            maps.at[AT, 'range0'] = temp['range0'].min()
            maps.at[AT, 'range1'] = temp['range1'].max()
            indexs.pop(0)
            drops.extend(indexs)
            
    maps = maps.drop(maps.index[drops])

    def shorted(x):
        if os.path.isabs(x):
           return os.path.basename(x).split('.')[0]
        else:
           if '[' in x: 
                x=x.replace('[','').replace(']','')
           return x

    maps['pathname'] = maps['pathname'].apply(lambda value : shorted(value))
    maps = maps.reset_index()

    # find biggest gap 
    maps['gap'] = maps['range0'].shift(-1) - maps['range1']
    maps['next_start'] = maps['range0'].shift(-1)
    COUNT_BREAKS = 3
    break_points = maps.sort_values(['gap'],ascending=[0]).head(COUNT_BREAKS)
    break_points = break_points.sort_values('range0', ascending=1)[[ 'range1', 'next_start']].to_numpy().tolist()

    maps = maps[['range0', 'range1', 'pathname']]
    maps.to_csv('./maps.csv')

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
    START_OF_ADDRESS = maps.range0.min()
    END_OF_ADDRESS = maps.range1.max() 

    subyranges = [rsyslog.address.min(),  1.4*pow(10, 14), rsyslog.address.max()]
    subyranges.extend( maps[maps['pathname'] == 'vsyscall'][['range0','range1']].to_numpy().tolist() [0])
    subyranges.extend( maps[maps['pathname'] == 'vvar'][['range0']].to_numpy().tolist() [0])
    subyranges.extend( maps[maps['pathname'] == 'vdso'][['range1']].to_numpy().tolist() [0])

    subyranges = sorted(subyranges)
    rsyslog['axis'] = pd.cut(x = rsyslog['address'], bins=subyranges)
    height_ratios = []
   
    for name, group in rsyslog.groupby('axis'):
        if len(group) > 0:
            height_ratios.append(len(group)*(name.right - name.left))

    DIGITS = len(str(int(min(height_ratios)))) - 1   
    height_ratios = map(lambda x : int(x/pow(10, DIGITS)) if DIGITS >=0 else 1, height_ratios)

    GRIDS = len(height_ratios)

    print height_ratios
    height_ratio = [2,3]
    fig, axes = plt.subplots(nrows=GRIDS, ncols = 1, sharex = True, gridspec_kw={'height_ratios': height_ratios, 'hspace' :0})
    
    for axis in axes:
        axis.spines['bottom'].set_visible(False)
        axis.spines['top'].set_visible(False)
    

    d = .015  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=axes[0].transAxes, color='k', clip_on=False)
    
    def set_color_list():
        return list(mcolors.TABLEAU_COLORS)

    color_list = set_color_list()
    colors=dict()
    def paint(label):
        colors.update({label : color_list.pop(-1)})

    map( lambda x:paint(x), rsyslog.label.unique().tolist())

    IDY = -1
    for name, partition  in rsyslog.groupby('axis'):
        if len(partition) > 0:
            #IDY = subyranges.index([name.left, name.right])
            IDY = IDY + 1
            CONVERTY = GRIDS-(IDY+1)
            for (area, mode), group in partition.groupby(['label', 'mode']):
                #(Anon, fault)
                print area, mode, len(group)
                axes[IDY].plot(group.timestamp, group.address, label=labels[mode], c=colors[area], marker=markers[mode], linestyle=' ', ms=1, zorder=zorders[mode])

            #axes[IDY].set_ylim(subyranges[converty][0]-PADDING, subyranges[converty][1]+PADDING)
            axes[IDY].set_ylim(partition.address.min(), partition.address.max())
            print (partition.address.min(), partition.address.max())

            #if IDY == 0:
            axes[IDY].spines['top'].set_visible(True)

            #if IDY == GRIDS-1:
            axes[IDY].spines['bottom'].set_visible(True)

            if IDY != GRIDS-1: 
                axes[IDY].set_xticks([])

            if IDY == 0:
                axes[IDY].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
                axes[IDY].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
            else:
                kwargs.update(transform=axes[IDY].transAxes)  # switch to the bottom axes
                axes[IDY].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
                axes[IDY].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
                axes[IDY].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
                axes[IDY].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal                        

    patches = [mpatches.Patch(color = value, label = '{} ({})'.format(key, len(rsyslog[rsyslog['label'] == key]))) for key, value in colors.iteritems()]
    patches.extend([mpatches.Patch(hatch = value, label = '{} ({})'.format(labels[key], len(rsyslog[rsyslog['mode']==key]))) for key, value in markers.iteritems()])
    legend = axes[0].legend(handles = patches, bbox_to_anchor=(1.05, 1))
    INDEX = "landscape"
    plt.suptitle('[{}] Virtual Address by timeline'.format(INDEX))
    plt.savefig("{}/{}.png".format(dir_path, INDEX),bbox_extra_artists=(legend,),bbox_inches='tight', format='png', dip=100)

    if os.environ.get('DISPLAY','') != '':
        plt.show()




draw_landscape('.')
